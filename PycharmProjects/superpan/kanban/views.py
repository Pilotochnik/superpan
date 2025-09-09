from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum, Count
from django.utils import timezone
from decimal import Decimal
from django_ratelimit.decorators import ratelimit
import json
import logging

from constants import MAX_JSON_SIZE, MAX_JSON_MOVE_SIZE

from .models import (
    KanbanBoard, KanbanColumn, ExpenseItem, ExpenseDocument, 
    ExpenseComment, ExpenseHistory, ExpenseCategory
)
from .forms import ExpenseItemForm, ExpenseDocumentForm, ExpenseCommentForm
from projects.models import Project, ProjectActivity

logger = logging.getLogger(__name__)


@login_required
def kanban_board(request, project_id):
    """Канбан-доска проекта"""
    project = get_object_or_404(Project, pk=project_id)
    
    # Проверяем доступ к проекту
    if not project.can_user_access(request.user):
        messages.error(request, 'У вас нет доступа к этому проекту.')
        return redirect('projects:dashboard')
    
    # Получаем или создаем канбан-доску
    board, created = KanbanBoard.objects.get_or_create(
        project=project,
        defaults={'created_by': request.user}
    )
    
    # Создаем стандартные колонки, если доска была только что создана
    if created:
        default_columns = [
            ('Новые', 'new', 0, '#f8f9fa'),
            ('К выполнению', 'todo', 1, '#e3f2fd'),
            ('В работе', 'in_progress', 2, '#fff3cd'),
            ('На проверке', 'review', 3, '#d1edff'),
            ('Выполнены', 'done', 4, '#d4edda'),
            ('Отменены', 'cancelled', 5, '#f8d7da'),
        ]
        
        for name, column_type, position, color in default_columns:
            KanbanColumn.objects.create(
                board=board,
                name=name,
                column_type=column_type,
                position=position,
                color=color
            )
    
    # Получаем колонки и элементы
    columns = board.columns.filter(is_active=True).prefetch_related(
        'items__created_by',
        'items__assigned_to',
        'items__category'
    )
    
    # Статистика задач
    total_expenses = ExpenseItem.objects.filter(project=project).aggregate(
        total_count=Count('id'),
        completed_count=Count('id', filter=Q(status='done')),
        in_progress_count=Count('id', filter=Q(status='in_progress')),
        new_count=Count('id', filter=Q(status='new')),
        total_hours=Sum('estimated_hours'),
        completed_hours=Sum('estimated_hours', filter=Q(status='done')),
    )
    
    # Вычисляем процент выполнения
    if total_expenses['total_count'] > 0:
        total_expenses['completion_percent'] = (total_expenses['completed_count'] / total_expenses['total_count']) * 100
    else:
        total_expenses['completion_percent'] = 0
    
    context = {
        'project': project,
        'board': board,
        'columns': columns,
        'categories': ExpenseCategory.objects.filter(is_active=True),
        'total_expenses': total_expenses,
        'can_manage': (
            request.user.is_superuser_role() or
            project.created_by == request.user or
            project.foreman == request.user
        ),
        'can_add_expenses': project.members.filter(
            user=request.user,
            can_add_expenses=True,
            is_active=True
        ).exists() or request.user.is_superuser_role()
    }
    
    return render(request, 'kanban/board.html', context)


@login_required
@ratelimit(key='user', rate='30/h', method='POST', block=True)
@require_http_methods(["POST"])
def create_expense_item(request, project_id):
    """Создание нового элемента расхода"""
    project = get_object_or_404(Project, pk=project_id)
    
    # Проверяем права на добавление расходов
    if not (request.user.is_superuser_role() or 
            project.members.filter(user=request.user, can_add_expenses=True, is_active=True).exists()):
        return JsonResponse({'error': 'Недостаточно прав'}, status=403)
    
    try:
        # Валидация размера JSON
        if len(request.body) > MAX_JSON_SIZE:
            return JsonResponse({'error': 'Слишком большой запрос'}, status=400)
        
        data = json.loads(request.body)
        
        # Валидация обязательных полей
        required_fields = ['title', 'estimated_hours']
        for field in required_fields:
            if field not in data or not data[field]:
                return JsonResponse({'error': f'Поле {field} обязательно'}, status=400)
        
        # Получаем канбан-доску
        board = KanbanBoard.objects.get(project=project)
        
        # Находим первую колонку (обычно "Ожидает")
        column = board.columns.filter(is_active=True).first()
        if not column:
            return JsonResponse({'error': 'Не найдена активная колонка'}, status=400)
        
        # Создаем задачу
        expense_item = ExpenseItem.objects.create(
            project=project,
            column=column,
            title=data.get('title'),
            description=data.get('description', ''),
            task_type=data.get('task_type', 'other'),
            estimated_hours=Decimal(str(data.get('estimated_hours', 0))),
            priority=data.get('priority', 'medium'),
            created_by=request.user,
            category_id=data.get('category_id') if data.get('category_id') else None
        )
        
        # Создаем запись в истории
        ExpenseHistory.objects.create(
            expense_item=expense_item,
            user=request.user,
            action='created',
            new_value=f"Создан элемент расхода на сумму {expense_item.amount} ₽"
        )
        
        # Создаем активность проекта
        ProjectActivity.objects.create(
            project=project,
            user=request.user,
            activity_type='expense_added',
            description=f'Добавлен расход "{expense_item.title}" на сумму {expense_item.amount} ₽'
        )
        
        return JsonResponse({
            'success': True,
            'item': {
                'id': str(expense_item.id),
                'title': expense_item.title,
                'description': expense_item.description,
                'amount': str(expense_item.amount),
                'expense_type': expense_item.get_expense_type_display(),
                'priority': expense_item.priority,
                'created_by': expense_item.created_by.get_full_name(),
                'created_at': expense_item.created_at.isoformat()
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Некорректные данные'}, status=400)
    except Exception as e:
        logger.error(f"Ошибка при создании элемента расхода: {e}")
        return JsonResponse({'error': 'Внутренняя ошибка сервера'}, status=500)


@login_required
@ratelimit(key='user', rate='60/h', method='POST', block=True)
@require_http_methods(["POST"])
def move_expense_item(request):
    """Перемещение элемента расхода между колонками"""
    try:
        # Валидация размера JSON
        if len(request.body) > MAX_JSON_MOVE_SIZE:
            return JsonResponse({'error': 'Слишком большой запрос'}, status=400)
        
        data = json.loads(request.body)
        item_id = data.get('item_id')
        target_column_id = data.get('target_column_id')
        position = data.get('position', 0)
        
        # Валидация обязательных полей
        if not item_id or not target_column_id:
            return JsonResponse({'error': 'Отсутствуют обязательные поля'}, status=400)
        
        expense_item = get_object_or_404(ExpenseItem, pk=item_id)
        target_column = get_object_or_404(KanbanColumn, pk=target_column_id)
        
        # Проверяем доступ к проекту
        if not expense_item.project.can_user_access(request.user):
            return JsonResponse({'error': 'Недостаточно прав'}, status=403)
        
        old_column = expense_item.column
        old_status = expense_item.status
        
        # Перемещаем элемент
        expense_item.column = target_column
        expense_item.position = position
        expense_item.save()
        
        # Создаем запись в истории
        ExpenseHistory.objects.create(
            expense_item=expense_item,
            user=request.user,
            action='moved',
            old_value=f"Колонка: {old_column.name}",
            new_value=f"Колонка: {target_column.name}",
            field_name='column'
        )
        
        # Если статус изменился на "одобрено", создаем соответствующую активность
        if old_status != expense_item.status and expense_item.status == 'approved':
            expense_item.approved_by = request.user
            expense_item.approved_at = timezone.now()
            expense_item.save(update_fields=['approved_by', 'approved_at'])
            
            ProjectActivity.objects.create(
                project=expense_item.project,
                user=request.user,
                activity_type='expense_approved',
                description=f'Одобрен расход "{expense_item.title}" на сумму {expense_item.amount} ₽'
            )
        
        return JsonResponse({'success': True})
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Некорректные данные'}, status=400)
    except Exception as e:
        logger.error(f"Ошибка при перемещении элемента: {e}")
        return JsonResponse({'error': 'Внутренняя ошибка сервера'}, status=500)


class ExpenseItemDetailView(LoginRequiredMixin, DetailView):
    """Детальный вид элемента расхода"""
    model = ExpenseItem
    template_name = 'kanban/expense_detail.html'
    context_object_name = 'expense_item'
    
    def get_object(self):
        expense_item = get_object_or_404(ExpenseItem, pk=self.kwargs['pk'])
        
        # Проверяем доступ к проекту
        if not expense_item.project.can_user_access(self.request.user):
            raise PermissionError("У вас нет доступа к этому проекту")
        
        return expense_item
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expense_item = self.object
        
        context['comments'] = expense_item.comments.select_related('author').order_by('created_at')
        context['documents'] = expense_item.documents.select_related('uploaded_by')
        context['history'] = expense_item.history.select_related('user')[:10]
        context['can_edit'] = (
            self.request.user.is_superuser_role() or
            expense_item.created_by == self.request.user or
            expense_item.project.can_user_access(self.request.user)
        )
        
        return context


@login_required
def edit_expense_item(request, pk):
    """Редактирование элемента расхода"""
    expense_item = get_object_or_404(ExpenseItem, pk=pk)
    
    # Проверяем права на редактирование
    if not (request.user.is_superuser_role() or 
            expense_item.created_by == request.user or
            expense_item.project.can_user_access(request.user)):
        messages.error(request, 'У вас нет прав для редактирования этого элемента.')
        return redirect('kanban:expense_detail', pk=pk)
    
    if request.method == 'POST':
        form = ExpenseItemForm(request.POST, instance=expense_item)
        if form.is_valid():
            old_amount = expense_item.amount
            expense_item = form.save()
            
            # Создаем запись в истории при изменении суммы
            if old_amount != expense_item.amount:
                ExpenseHistory.objects.create(
                    expense_item=expense_item,
                    user=request.user,
                    action='updated',
                    old_value=f"Сумма: {old_amount}",
                    new_value=f"Сумма: {expense_item.amount}",
                    field_name='amount'
                )
            
            messages.success(request, 'Элемент расхода успешно обновлен.')
            return redirect('kanban:expense_detail', pk=pk)
    else:
        form = ExpenseItemForm(instance=expense_item)
    
    return render(request, 'kanban/expense_form.html', {
        'form': form,
        'expense_item': expense_item,
        'title': f'Редактировать "{expense_item.title}"'
    })


@login_required
@require_http_methods(["POST"])
def add_expense_comment(request, pk):
    """Добавление комментария к элементу расхода"""
    expense_item = get_object_or_404(ExpenseItem, pk=pk)
    
    # Проверяем доступ к проекту
    if not expense_item.project.can_user_access(request.user):
        return JsonResponse({'error': 'Недостаточно прав'}, status=403)
    
    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        
        if not text:
            return JsonResponse({'error': 'Комментарий не может быть пустым'}, status=400)
        
        comment = ExpenseComment.objects.create(
            expense_item=expense_item,
            author=request.user,
            text=text,
            is_internal=data.get('is_internal', False)
        )
        
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'text': comment.text,
                'author': comment.author.get_full_name(),
                'created_at': comment.created_at.isoformat(),
                'is_internal': comment.is_internal
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Некорректные данные'}, status=400)
    except Exception as e:
        logger.error(f"Ошибка при добавлении комментария: {e}")
        return JsonResponse({'error': 'Внутренняя ошибка сервера'}, status=500)


@login_required
@require_http_methods(["POST"])
def reject_expense_item(request, pk):
    """Отклонение элемента расхода"""
    expense_item = get_object_or_404(ExpenseItem, pk=pk)
    
    # Проверяем права (только менеджеры проекта могут отклонять)
    if not (request.user.is_superuser_role() or 
            expense_item.project.created_by == request.user or
            expense_item.project.foreman == request.user):
        return JsonResponse({'error': 'Недостаточно прав'}, status=403)
    
    try:
        data = json.loads(request.body)
        reason = data.get('reason', '').strip()
        
        if not reason:
            return JsonResponse({'error': 'Укажите причину отклонения'}, status=400)
        
        # Перемещаем в колонку "Отклонено"
        rejected_column = expense_item.project.kanban_board.columns.filter(
            column_type='rejected'
        ).first()
        
        if rejected_column:
            expense_item.column = rejected_column
            expense_item.rejection_reason = reason
            expense_item.save()
            
            # Создаем активность
            ProjectActivity.objects.create(
                project=expense_item.project,
                user=request.user,
                activity_type='expense_rejected',
                description=f'Отклонен расход "{expense_item.title}" на сумму {expense_item.amount} ₽'
            )
            
            # Добавляем комментарий с причиной отклонения
            ExpenseComment.objects.create(
                expense_item=expense_item,
                author=request.user,
                text=f"Расход отклонен. Причина: {reason}",
                is_internal=True
            )
            
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Не найдена колонка для отклоненных элементов'}, status=500)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Некорректные данные'}, status=400)
    except Exception as e:
        logger.error(f"Ошибка при отклонении элемента: {e}")
        return JsonResponse({'error': 'Внутренняя ошибка сервера'}, status=500)


@login_required
def expense_analytics(request, project_id):
    """Аналитика расходов проекта"""
    project = get_object_or_404(Project, pk=project_id)
    
    # Проверяем доступ к проекту
    if not project.can_user_access(request.user):
        messages.error(request, 'У вас нет доступа к этому проекту.')
        return redirect('projects:dashboard')
    
    # Собираем статистику
    expenses_by_type = ExpenseItem.objects.filter(project=project).values(
        'expense_type'
    ).annotate(
        total_amount=Sum('amount'),
        count=Count('id')
    ).order_by('-total_amount')
    
    expenses_by_status = ExpenseItem.objects.filter(project=project).values(
        'status'
    ).annotate(
        total_amount=Sum('amount'),
        count=Count('id')
    )
    
    expenses_by_category = ExpenseItem.objects.filter(
        project=project,
        category__isnull=False
    ).values(
        'category__name',
        'category__color'
    ).annotate(
        total_amount=Sum('amount'),
        count=Count('id')
    ).order_by('-total_amount')
    
    context = {
        'project': project,
        'expenses_by_type': expenses_by_type,
        'expenses_by_status': expenses_by_status,
        'expenses_by_category': expenses_by_category,
        'total_budget': project.budget,
        'total_spent': project.spent_amount,
        'remaining_budget': project.remaining_budget
    }
    
    return render(request, 'kanban/analytics.html', context)


@login_required
@require_http_methods(["POST"])
def add_expense(request):
    """Добавление нового расхода"""
    try:
        # Получаем данные из формы
        project_id = request.POST.get('project_id')
        if not project_id:
            return JsonResponse({'error': 'Не указан проект'}, status=400)
        
        project = get_object_or_404(Project, pk=project_id)
        
        # Проверяем доступ к проекту
        if not project.can_user_access(request.user):
            return JsonResponse({'error': 'У вас нет доступа к этому проекту'}, status=403)
        
        # Проверяем права на добавление расходов
        can_add = (
            request.user.is_superuser_role() or
            project.created_by == request.user or
            project.foreman == request.user or
            request.user.role == 'contractor'
        )
        
        if not can_add:
            return JsonResponse({'error': 'Недостаточно прав для добавления расходов'}, status=403)
        
        # Получаем данные формы
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        expense_type = request.POST.get('expense_type', 'other')
        amount = request.POST.get('amount', '0')
        priority = request.POST.get('priority', 'medium')
        
        # Валидация
        if not title:
            return JsonResponse({'error': 'Название расхода обязательно'}, status=400)
        
        try:
            amount = Decimal(amount)
            if amount <= 0:
                return JsonResponse({'error': 'Сумма должна быть больше 0'}, status=400)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Неверная сумма'}, status=400)
        
        # Получаем или создаем канбан-доску
        board, created = KanbanBoard.objects.get_or_create(
            project=project,
            defaults={'created_by': request.user}
        )
        
        # Получаем колонку "Ожидает"
        column = board.columns.filter(column_type='pending').first()
        if not column:
            # Создаем колонку если её нет
            column = KanbanColumn.objects.create(
                board=board,
                name='Ожидает',
                column_type='pending',
                position=0
            )
        
        # Создаем задачу
        expense = ExpenseItem.objects.create(
            project=project,
            column=column,
            title=title,
            description=description,
            task_type=expense_type,
            estimated_hours=amount,
            priority=priority,
            created_by=request.user
        )
        
        # Обрабатываем файлы
        if 'receipt_file' in request.FILES:
            expense.receipt_file = request.FILES['receipt_file']
        
        if 'photo_files' in request.FILES:
            expense.photo_files = request.FILES['photo_files']
        
        expense.save()
        
        # Создаем активность
        ProjectActivity.objects.create(
            project=project,
            user=request.user,
            activity_type='expense_added',
            description=f'Добавлен расход: {title} на сумму {amount} ₽'
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Расход успешно добавлен',
            'expense_id': str(expense.id)
        })
        
    except Exception as e:
        logger.error(f"Error adding expense: {e}")
        return JsonResponse({'error': 'Ошибка сервера'}, status=500)
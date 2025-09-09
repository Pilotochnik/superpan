from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    ExpenseCategory, ExpenseItem, ExpenseHistory, ExpenseDocument, 
    ExpenseComment, KanbanBoard, KanbanColumn
)
from .task_models import (
    TaskCategory, TaskPriority, TaskStatus, ProjectTask, 
    TaskComment, TaskAttachment, TaskHistory, TaskDependency
)


class ExpenseDocumentInline(admin.TabularInline):
    model = ExpenseDocument
    extra = 0


class ExpenseCommentInline(admin.TabularInline):
    model = ExpenseComment
    extra = 0


@admin.register(ExpenseItem)
class ExpenseItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'task_type', 'estimated_hours', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'task_type', 'created_at')
    search_fields = ('title', 'description', 'project__name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ExpenseDocumentInline, ExpenseCommentInline]
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('title', 'description', 'task_type', 'project')
        }),
        (_('Задача'), {
            'fields': ('estimated_hours', 'progress_percent', 'due_date', 'is_urgent', 'tags')
        }),
        (_('Управление'), {
            'fields': ('status', 'priority', 'created_by', 'assigned_to')
        }),
    )


@admin.register(ExpenseDocument)
class ExpenseDocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'expense_item', 'file_type', 'uploaded_by', 'created_at')
    list_filter = ('file_type', 'created_at')
    search_fields = ('name', 'expense_item__title')
    readonly_fields = ('created_at',)


@admin.register(ExpenseHistory)
class ExpenseHistoryAdmin(admin.ModelAdmin):
    list_display = ('expense_item', 'action', 'user', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('expense_item__title', 'user__email')
    readonly_fields = ('created_at',)


@admin.register(ExpenseComment)
class ExpenseCommentAdmin(admin.ModelAdmin):
    list_display = ('expense_item', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('expense_item__title', 'author__email')
    readonly_fields = ('created_at',)


@admin.register(KanbanBoard)
class KanbanBoardAdmin(admin.ModelAdmin):
    list_display = ('project', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('project__name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(KanbanColumn)
class KanbanColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'board', 'position', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    readonly_fields = ()


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)


# Админка для задач
class TaskCommentInline(admin.TabularInline):
    model = TaskComment
    extra = 0
    readonly_fields = ('created_at',)


class TaskAttachmentInline(admin.TabularInline):
    model = TaskAttachment
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'icon', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)


@admin.register(TaskPriority)
class TaskPriorityAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'color', 'icon', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('level',)


@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'icon', 'is_final', 'order', 'is_active')
    list_filter = ('is_final', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('order', 'name')


@admin.register(ProjectTask)
class ProjectTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'priority', 'assigned_to', 'progress_percent', 'due_date', 'created_at')
    list_filter = ('status', 'priority', 'task_type', 'is_urgent', 'is_blocked', 'created_at')
    search_fields = ('title', 'description', 'project__name', 'tags')
    readonly_fields = ('created_at', 'updated_at', 'id')
    inlines = [TaskCommentInline, TaskAttachmentInline]
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('title', 'description', 'project', 'task_type', 'tags')
        }),
        (_('Классификация'), {
            'fields': ('category', 'priority', 'status')
        }),
        (_('Назначение'), {
            'fields': ('created_by', 'assigned_to', 'reviewed_by')
        }),
        (_('Сроки'), {
            'fields': ('due_date', 'started_at', 'completed_at')
        }),
        (_('Прогресс'), {
            'fields': ('progress_percent', 'estimated_hours', 'actual_hours')
        }),
        (_('Финансы'), {
            'fields': ('budget', 'actual_cost')
        }),
        (_('Канбан'), {
            'fields': ('column', 'position')
        }),
        (_('Дополнительно'), {
            'fields': ('is_urgent', 'is_blocked', 'block_reason', 'attachment')
        }),
    )


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author', 'is_internal', 'is_system', 'created_at')
    list_filter = ('is_internal', 'is_system', 'created_at')
    search_fields = ('task__title', 'author__email', 'text')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(TaskAttachment)
class TaskAttachmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'task', 'uploaded_by', 'file_size', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'task__title', 'uploaded_by__email')
    readonly_fields = ('created_at', 'file_size')


@admin.register(TaskHistory)
class TaskHistoryAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'action', 'field_name', 'created_at')
    list_filter = ('action', 'field_name', 'created_at')
    search_fields = ('task__title', 'user__email')
    readonly_fields = ('created_at',)


@admin.register(TaskDependency)
class TaskDependencyAdmin(admin.ModelAdmin):
    list_display = ('task', 'depends_on', 'dependency_type', 'created_at')
    list_filter = ('dependency_type', 'created_at')
    search_fields = ('task__title', 'depends_on__title')
    readonly_fields = ('created_at',)
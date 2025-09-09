from django.urls import path
from . import views, task_views

app_name = 'kanban'

urlpatterns = [
    # Старые URL для расходов (для совместимости)
    path('board/<uuid:project_id>/', views.kanban_board, name='board'),
    path('expense/<uuid:pk>/', views.ExpenseItemDetailView.as_view(), name='expense_detail'),
    path('expense/<uuid:pk>/edit/', views.edit_expense_item, name='expense_edit'),
    path('api/create-expense/<uuid:project_id>/', views.create_expense_item, name='create_expense'),
    path('api/move-expense/', views.move_expense_item, name='move_expense'),
    path('api/add-comment/<uuid:pk>/', views.add_expense_comment, name='add_comment'),
    path('api/reject-expense/<uuid:pk>/', views.reject_expense_item, name='reject_expense'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('analytics/<uuid:project_id>/', views.expense_analytics, name='analytics'),
    
    # Новые URL для задач
    path('tasks/<uuid:project_id>/', task_views.task_board, name='task_board'),
    path('tasks/<uuid:project_id>/list/', task_views.task_list, name='task_list'),
    path('tasks/<uuid:project_id>/create/', task_views.create_task, name='create_task'),
    path('tasks/<uuid:project_id>/<uuid:task_id>/', task_views.task_detail, name='task_detail'),
    path('tasks/<uuid:project_id>/<uuid:task_id>/edit/', task_views.edit_task, name='edit_task'),
    path('tasks/<uuid:project_id>/<uuid:task_id>/comment/', task_views.add_comment, name='add_comment'),
    path('tasks/<uuid:project_id>/<uuid:task_id>/progress/', task_views.update_progress, name='update_progress'),
    path('tasks/<uuid:project_id>/<uuid:task_id>/assign/', task_views.assign_task, name='assign_task'),
    path('tasks/<uuid:project_id>/<uuid:task_id>/move/', task_views.move_task, name='move_task'),
    path('tasks/<uuid:project_id>/analytics/', task_views.task_analytics, name='task_analytics'),
]

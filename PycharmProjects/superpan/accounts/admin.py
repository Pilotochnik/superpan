from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserSession, ProjectAccessKey, LoginAttempt


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        (_('Личная информация'), {
            'fields': ('first_name', 'last_name', 'phone', 'role')
        }),
        (_('Разрешения'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (_('Важные даты'), {
            'fields': ('last_login', 'created_at'),
        }),
    )
    readonly_fields = ('created_at', 'last_login')


@admin.register(ProjectAccessKey)
class ProjectAccessKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'project_id', 'assigned_to', 'created_by', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('key', 'assigned_to__email', 'created_by__email')
    readonly_fields = ('key', 'created_at', 'used_at')


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key', 'ip_address', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'ip_address')
    readonly_fields = ('created_at', 'last_activity')


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('email', 'ip_address', 'success', 'created_at')
    list_filter = ('success', 'created_at')
    search_fields = ('email', 'ip_address')
    readonly_fields = ('created_at',)
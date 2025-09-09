from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import hashlib
import uuid
import logging

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    """Кастомный менеджер пользователей"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        extra_fields.setdefault('username', email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.SUPERUSER)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Кастомная модель пользователя с ролями и привязкой к устройству"""
    
    class Role(models.TextChoices):
        SUPERUSER = 'superuser', _('Суперпользователь')
        FOREMAN = 'foreman', _('Прораб')
        CONTRACTOR = 'contractor', _('Подрядчик')
    
    email = models.EmailField(_('Email адрес'), unique=True)
    role = models.CharField(
        _('Роль'),
        max_length=20,
        choices=Role.choices,
        default=Role.CONTRACTOR
    )
    phone = models.CharField(_('Телефон'), max_length=20, blank=True)
    is_active_session = models.BooleanField(_('Активная сессия'), default=False)
    device_fingerprint = models.CharField(
        _('Отпечаток устройства'),
        max_length=128,
        blank=True,
        help_text=_('Уникальный идентификатор устройства пользователя')
    )
    last_login_ip = models.GenericIPAddressField(_('Последний IP'), blank=True, null=True)
    failed_login_attempts = models.PositiveIntegerField(_('Неудачные попытки входа'), default=0)
    locked_until = models.DateTimeField(_('Заблокирован до'), blank=True, null=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        db_table = 'users'

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email

    def is_superuser_role(self):
        return self.role == self.Role.SUPERUSER

    def is_foreman_role(self):
        return self.role == self.Role.FOREMAN

    def is_contractor_role(self):
        return self.role == self.Role.CONTRACTOR

    def can_manage_projects(self):
        """Может ли пользователь управлять проектами"""
        return self.role in [self.Role.SUPERUSER, self.Role.FOREMAN]

    def generate_device_fingerprint(self, user_agent, ip_address):
        """Генерирует отпечаток устройства на основе user-agent и IP"""
        data = f"{user_agent}_{ip_address}_{self.email}"
        return hashlib.sha256(data.encode()).hexdigest()

    def is_device_allowed(self, user_agent, ip_address):
        """Проверяет, разрешено ли устройство для этого пользователя"""
        if not self.device_fingerprint:
            return True  # Первый вход
        
        current_fingerprint = self.generate_device_fingerprint(user_agent, ip_address)
        return self.device_fingerprint == current_fingerprint

    def bind_device(self, user_agent, ip_address):
        """Привязывает пользователя к устройству"""
        self.device_fingerprint = self.generate_device_fingerprint(user_agent, ip_address)
        self.last_login_ip = ip_address
        self.save(update_fields=['device_fingerprint', 'last_login_ip'])
    
    def get_accessible_projects(self):
        """Получить все доступные пользователю проекты"""
        from projects.models import Project
        from django.db.models import Q
        
        if self.is_superuser_role():
            return Project.objects.filter(is_active=True)
        elif self.is_foreman_role():
            return Project.objects.filter(
                Q(created_by=self) | Q(foreman=self),
                is_active=True
            ).distinct()
        else:
            # Подрядчики видят проекты через ключи доступа
            access_keys = ProjectAccessKey.objects.filter(
                assigned_to=self,
                is_active=True
            ).values_list('project_id', flat=True)
            
            return Project.objects.filter(
                id__in=access_keys,
                is_active=True
            ).distinct()


class UserSession(models.Model):
    """Модель для отслеживания активных сессий пользователей"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь'),
        related_name='active_session'
    )
    session_key = models.CharField(_('Ключ сессии'), max_length=40, unique=True)
    device_info = models.TextField(_('Информация об устройстве'), blank=True)
    ip_address = models.GenericIPAddressField(_('IP адрес'))
    created_at = models.DateTimeField(_('Создано'), auto_now_add=True)
    last_activity = models.DateTimeField(_('Последняя активность'), auto_now=True)

    class Meta:
        verbose_name = _('Сессия пользователя')
        verbose_name_plural = _('Сессии пользователей')
        db_table = 'user_sessions'

    def __str__(self):
        return f"Сессия {self.user.email}"


class ProjectAccessKey(models.Model):
    """Модель для ключей доступа к проектам"""
    
    key = models.UUIDField(_('Ключ доступа'), default=uuid.uuid4, unique=True)
    project_id = models.UUIDField(_('ID проекта'))
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Создал'),
        related_name='created_access_keys'
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Назначен'),
        related_name='assigned_access_keys',
        blank=True,
        null=True
    )
    description = models.TextField(_('Описание'), blank=True, help_text=_('Описание цели предоставления доступа'))
    is_active = models.BooleanField(_('Активен'), default=True)
    expires_at = models.DateTimeField(_('Истекает'), blank=True, null=True)
    created_at = models.DateTimeField(_('Создан'), auto_now_add=True)
    used_at = models.DateTimeField(_('Использован'), blank=True, null=True)

    class Meta:
        verbose_name = _('Ключ доступа к проекту')
        verbose_name_plural = _('Ключи доступа к проектам')
        db_table = 'project_access_keys'
        # Убираем unique_together чтобы можно было создавать несколько ключей
        # но логика в коде будет контролировать активные ключи

    def __str__(self):
        try:
            from projects.models import Project
            project = Project.objects.get(id=self.project_id)
            return f"Ключ для {project.name}"
        except Project.DoesNotExist:
            return f"Ключ доступа {str(self.key)[:8]}... (проект не найден)"
        except Exception as e:
            logger.error(f"Ошибка при получении проекта для ключа {self.key}: {e}")
            return f"Ключ доступа {str(self.key)[:8]}... (ошибка)"

    def is_valid(self):
        """Проверяет, действителен ли ключ"""
        if not self.is_active:
            return False
        
        if self.expires_at and self.expires_at < timezone.now():
            return False
            
        return True


class LoginAttempt(models.Model):
    """Модель для отслеживания попыток входа"""
    
    email = models.EmailField(_('Email'))
    ip_address = models.GenericIPAddressField(_('IP адрес'))
    user_agent = models.TextField(_('User Agent'), blank=True)
    success = models.BooleanField(_('Успешно'), default=False)
    failure_reason = models.CharField(_('Причина неудачи'), max_length=100, blank=True)
    created_at = models.DateTimeField(_('Время попытки'), auto_now_add=True)

    class Meta:
        verbose_name = _('Попытка входа')
        verbose_name_plural = _('Попытки входа')
        db_table = 'login_attempts'
        ordering = ['-created_at']

    def __str__(self):
        status = "Успешно" if self.success else "Неудачно"
        return f"{self.email} - {status} ({self.created_at})"

# 🏗️ Проектный Офис - Система управления строительными проектами

**Проектный Офис** - это современная веб-платформа для управления строительными проектами с высоким уровнем безопасности, канбан-досками для управления расходами и системой ролей для эффективной работы команды.

## ✨ Основные возможности

### 🎯 **Для бизнеса**
- **Управление проектами** с бюджетированием и контролем расходов
- **Канбан-доски** для визуального управления сметами и расходами
- **Система ролей**: Администратор → Прораб → Подрядчики
- **Ключи доступа** для безопасного предоставления доступа к проектам
- **Аналитика и отчеты** по проектам и расходам

### 🔒 **Безопасность**
- **Привязка к устройству** - каждый пользователь может работать только с одного устройства
- **Отслеживание входов** и блокировка подозрительной активности
- **Управление сессиями** с автоматическим завершением неактивных сессий
- **Логирование всех действий** для аудита безопасности

### 📊 **Канбан-система**
- **5 колонок**: Ожидает → На рассмотрении → Одобрено → Отклонено → Оплачено
- **Drag & Drop** перемещение расходов между статусами
- **Типы расходов**: Материалы, Работы, Транспорт, Топливо, Оборудование
- **Категории расходов** с цветовой кодировкой
- **Комментарии и документы** к каждому расходу

## 🚀 Быстрый старт

### Автоматическая установка (рекомендуется)

```bash
# Скачайте проект
git clone <repository-url>
cd superpan

# Запустите автоматический скрипт установки
python setup_superpan.py
```

Скрипт автоматически:
- ✅ Создаст виртуальное окружение
- ✅ Установит все зависимости
- ✅ Настроит базу данных
- ✅ Создаст суперпользователя
- ✅ Создаст демо-данные
- ✅ Запустит сервер

### Ручная установка

```bash
# 1. Создание виртуального окружения
python -m venv venv

# 2. Активация окружения
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Установка зависимостей
pip install -r requirements.txt

# 4. Настройка базы данных
python manage.py makemigrations
python manage.py migrate

# 5. Создание суперпользователя
python manage.py create_demo_superuser

# 6. Создание демо-данных (опционально)
python manage.py create_demo_data

# 7. Запуск сервера
python manage.py runserver
```

## 👥 Учетные данные по умолчанию

После установки доступны следующие аккаунты:

| Роль | Email | Пароль | Описание |
|------|-------|---------|----------|
| **Администратор** | `admin@superpan.ru` | `admin123` | Полный доступ к системе |
| **Прораб** | `foreman@superpan.ru` | `foreman123` | Управление проектами |
| **Подрядчик 1** | `contractor1@superpan.ru` | `contractor123` | Добавление расходов |
| **Подрядчик 2** | `contractor2@superpan.ru` | `contractor123` | Добавление расходов |
| **Подрядчик 3** | `contractor3@superpan.ru` | `contractor123` | Добавление расходов |

## 🌐 Доступные страницы

| URL | Описание | Доступ |
|-----|----------|---------|
| `http://127.0.0.1:8000/` | Главная система | Все пользователи |
| `http://127.0.0.1:8000/projects/` | Управление проектами | Все пользователи |
| `http://127.0.0.1:8000/kanban/board/{id}/` | Канбан-доска проекта | Участники проекта |
| `http://127.0.0.1:8000/management/` | Простая админка | Только администраторы |
| `http://127.0.0.1:8000/admin/` | Django админка | Только администраторы |

## 📋 Сценарий использования

### 1. **Администратор создает проект**
```
Бюджет: 1,000,000 ₽
Прораб: Иван Прорабов
Адрес: г. Москва, ул. Строительная, д. 15
```

### 2. **Выдача доступа подрядчикам**
```
Администратор → Админка → Ключи доступа → Создать ключ
Подрядчик → Профиль → Использовать ключ доступа
```

### 3. **Работа с расходами**
```
Подрядчик добавляет расход → Колонка "Ожидает"
Прораб проверяет → Перетаскивает в "На рассмотрении"
Прораб одобряет → Перетаскивает в "Одобрено"
Бухгалтерия → Перетаскивает в "Оплачено"
```

## 🏗️ Архитектура системы

```
SuperPan/
├── accounts/          # Управление пользователями и безопасность
│   ├── models.py      # User, ProjectAccessKey, LoginAttempt
│   ├── views.py       # Аутентификация, профили
│   ├── middleware.py  # Безопасность устройств
│   └── management/    # Команды создания данных
├── projects/          # Управление проектами
│   ├── models.py      # Project, ProjectMember, ProjectActivity
│   └── views.py       # CRUD проектов
├── kanban/           # Канбан-система
│   ├── models.py     # KanbanBoard, ExpenseItem, ExpenseCategory
│   └── views.py      # Канбан-доска, управление расходами
├── admin_panel/      # Простая админка
│   ├── views.py      # Управление пользователями и проектами
│   └── templates/    # Простые шаблоны админки
└── templates/        # Фронтенд шаблоны
    ├── base.html     # Базовый шаблон
    ├── accounts/     # Шаблоны аутентификации
    ├── projects/     # Шаблоны проектов
    └── kanban/       # Шаблоны канбан-досок
```

## 🔧 Технические детали

### Стек технологий
- **Backend**: Django 5.2, Python 3.8+
- **Database**: SQLite (для разработки), PostgreSQL (для продакшена)
- **Frontend**: Bootstrap 5, Vanilla JavaScript
- **Security**: Custom middleware, device binding, session management

### Модели данных

#### User (Пользователь)
```python
- email (unique)
- role: superuser | foreman | contractor
- device_fingerprint (для привязки к устройству)
- failed_login_attempts, locked_until
```

#### Project (Проект)
```python
- name, description, address
- budget (Decimal)
- status: planning | active | on_hold | completed
- foreman (ForeignKey to User)
```

#### ExpenseItem (Расход)
```python
- title, description, amount
- expense_type: material | labor | transport | fuel | equipment
- status: pending | in_review | approved | rejected | paid
- priority: low | medium | high
```

### Безопасность

#### Привязка к устройству
```python
def is_device_allowed(self, user_agent, ip_address):
    """Проверяет разрешенность устройства"""
    if not self.device_fingerprint:
        return True  # Первый вход
    current_fingerprint = self.generate_device_fingerprint(user_agent, ip_address)
    return self.device_fingerprint == current_fingerprint
```

#### Middleware безопасности
- `DeviceTrackingMiddleware` - проверка устройств
- `SessionSecurityMiddleware` - тайм-ауты сессий
- `SingleSessionMiddleware` - одна сессия на пользователя

## 📊 API и интеграции

### AJAX API для канбан-доски
```javascript
// Создание расхода
POST /kanban/api/create-expense/{project_id}/
{
    "title": "Закупка цемента",
    "amount": 25000,
    "expense_type": "material",
    "priority": "high"
}

// Перемещение расхода
POST /kanban/api/move-expense/
{
    "item_id": "uuid",
    "target_column_id": "uuid",
    "position": 0
}
```

## 🧪 Тестирование

### Запуск тестов
```bash
python manage.py test
```

### Создание тестовых данных
```bash
# Очистка и создание новых данных
python manage.py create_demo_data --clear

# Только создание суперпользователя
python manage.py create_demo_superuser --email admin@test.ru --password test123
```

## 🚀 Деплой в продакшн

### 1. Настройка переменных окружения
```bash
# Скопируйте env.example в .env и настройте
cp env.example .env

# .env файл для продакшена
DEBUG=False
SECRET_KEY=your-super-secret-key-here-change-this
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost/superpan
```

### 2. Проверка безопасности
```bash
# Запустите проверку безопасности
python check_security.py
```

### 2. Настройка PostgreSQL
```python
# settings.py
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}
```

### 3. Сборка статики
```bash
python manage.py collectstatic --noinput
```

### 4. Запуск с Gunicorn
```bash
gunicorn superpan.wsgi:application --bind 0.0.0.0:8000
```

## 🛠️ Разработка

### Добавление новых функций

1. **Новый тип расхода**
```python
# kanban/models.py
class ExpenseItem(models.Model):
    class ExpenseType(models.TextChoices):
        # Добавить новый тип
        NEW_TYPE = 'new_type', _('Новый тип')
```

2. **Новая роль пользователя**
```python
# accounts/models.py
class User(AbstractUser):
    class Role(models.TextChoices):
        # Добавить новую роль
        NEW_ROLE = 'new_role', _('Новая роль')
```

### Кастомизация интерфейса

Все шаблоны находятся в `templates/` и используют Bootstrap 5:
- `templates/base.html` - базовый шаблон
- `templates/kanban/board.html` - канбан-доска
- `templates/admin_panel/` - простая админка

## 📞 Поддержка

### Часто задаваемые вопросы

**Q: Как сбросить привязку к устройству?**
A: Администратор может сбросить через админку или API: `POST /accounts/reset-device/`

**Q: Как добавить нового пользователя?**
A: Через простую админку `/management/users/create/` или Django админку

**Q: Как создать новый проект?**
A: Администраторы и прорабы могут создавать проекты через `/projects/create/`

**Q: Как выдать доступ к проекту?**
A: Через админку создать ключ доступа, пользователь вводит ключ в профиле

### Логи и отладка

```bash
# Просмотр логов входов
python manage.py shell
>>> from accounts.models import LoginAttempt
>>> LoginAttempt.objects.filter(success=False)

# Просмотр активных сессий
>>> from accounts.models import UserSession
>>> UserSession.objects.all()
```

## 📄 Лицензия

Этот проект создан для управления строительными проектами и демонстрации возможностей Django.

---

## 🎯 Готово к использованию!

SuperPan полностью готов к работе. Запустите `python setup_superpan.py` и начинайте управлять своими строительными проектами! 🚀
"""
Константы для проекта SuperPan
"""

# Размеры файлов
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 МБ
MAX_JSON_SIZE = 10 * 1024  # 10 КБ для JSON запросов
MAX_JSON_MOVE_SIZE = 5 * 1024  # 5 КБ для перемещения элементов

# Лимиты безопасности
MAX_LOGIN_ATTEMPTS = 5
LOGIN_BLOCK_DURATION_MINUTES = 15
MAX_COMMENT_LENGTH = 2000
MAX_FIELDS_PER_FORM = 1000

# Время жизни сессий
SESSION_TIMEOUT_MINUTES = 30
CSRF_TOKEN_AGE_HOURS = 24

# Rate limiting
RATE_LIMIT_LOGIN = '5/m'
RATE_LIMIT_ACCESS_KEY = '20/h'
RATE_LIMIT_RESET_DEVICE = '10/h'
RATE_LIMIT_CREATE_EXPENSE = '30/h'
RATE_LIMIT_MOVE_EXPENSE = '60/h'
RATE_LIMIT_GENERATE_KEY = '10/h'

# Пагинация
PROJECTS_PER_PAGE = 12
ACTIVITIES_PER_PAGE = 10
DOCUMENTS_PER_PAGE = 5

# Статусы проектов
PROJECT_STATUS_PLANNING = 'planning'
PROJECT_STATUS_IN_PROGRESS = 'in_progress'
PROJECT_STATUS_ON_HOLD = 'on_hold'
PROJECT_STATUS_COMPLETED = 'completed'
PROJECT_STATUS_CANCELLED = 'cancelled'

# Роли пользователей
USER_ROLE_SUPERUSER = 'superuser'
USER_ROLE_FOREMAN = 'foreman'
USER_ROLE_CONTRACTOR = 'contractor'

# Типы расходов
EXPENSE_TYPE_MATERIAL = 'material'
EXPENSE_TYPE_LABOR = 'labor'
EXPENSE_TYPE_TRANSPORT = 'transport'
EXPENSE_TYPE_FUEL = 'fuel'
EXPENSE_TYPE_EQUIPMENT = 'equipment'

# Статусы расходов
EXPENSE_STATUS_PENDING = 'pending'
EXPENSE_STATUS_IN_REVIEW = 'in_review'
EXPENSE_STATUS_APPROVED = 'approved'
EXPENSE_STATUS_REJECTED = 'rejected'
EXPENSE_STATUS_PAID = 'paid'

# Приоритеты
PRIORITY_LOW = 'low'
PRIORITY_MEDIUM = 'medium'
PRIORITY_HIGH = 'high'

# Разрешенные типы файлов
ALLOWED_FILE_EXTENSIONS = [
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', 
    '.jpg', '.jpeg', '.png', '.gif'
]

ALLOWED_MIME_TYPES = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'image/jpeg',
    'image/png',
    'image/gif'
]

# Опасные паттерны для XSS защиты
DANGEROUS_XSS_PATTERNS = [
    r'<script[^>]*>.*?</script>',
    r'<iframe[^>]*>.*?</iframe>',
    r'<object[^>]*>.*?</object>',
    r'<embed[^>]*>',
    r'<link[^>]*>',
    r'<meta[^>]*>',
    r'javascript:',
    r'vbscript:',
    r'data:',
]

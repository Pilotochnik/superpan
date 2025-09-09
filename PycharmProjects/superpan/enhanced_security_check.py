#!/usr/bin/env python
"""
🔐 УЛУЧШЕННАЯ ПРОВЕРКА БЕЗОПАСНОСТИ SUPERPAN
Проверяет все критические аспекты безопасности
"""
import os
import sys
import django
from pathlib import Path
import re

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'superpan.settings')
django.setup()

from django.conf import settings

def check_security_settings():
    """Проверяет настройки безопасности"""
    print("🔐 ПРОВЕРКА НАСТРОЕК БЕЗОПАСНОСТИ")
    print("=" * 50)
    
    issues = []
    warnings = []
    
    # 1. Проверка DEBUG режима
    if settings.DEBUG:
        warnings.append("⚠️ DEBUG=True - отключите в продакшене!")
    else:
        print("✅ DEBUG=False")
    
    # 2. Проверка SECRET_KEY
    if settings.SECRET_KEY == 'django-insecure-change-this-in-production':
        issues.append("❌ SECRET_KEY не изменен - используйте случайный ключ!")
    else:
        print("✅ SECRET_KEY настроен")
    
    # 3. Проверка ALLOWED_HOSTS
    if settings.DEBUG:
        if '*' in settings.ALLOWED_HOSTS:
            issues.append("❌ ALLOWED_HOSTS содержит '*' в режиме разработки!")
        else:
            print("✅ ALLOWED_HOSTS безопасен для разработки")
    else:
        if not settings.ALLOWED_HOSTS or settings.ALLOWED_HOSTS == ['']:
            issues.append("❌ ALLOWED_HOSTS не настроен для продакшена!")
        else:
            print("✅ ALLOWED_HOSTS настроен для продакшена")
    
    # 4. Проверка HTTPS настроек
    if not settings.DEBUG:
        if not settings.SECURE_SSL_REDIRECT:
            warnings.append("⚠️ SECURE_SSL_REDIRECT=False в продакшене")
        else:
            print("✅ SECURE_SSL_REDIRECT=True")
        
        if not settings.SECURE_COOKIES:
            warnings.append("⚠️ Не все cookies защищены")
        else:
            print("✅ Cookies защищены")
    
    # 5. Проверка CSRF защиты
    if 'django.middleware.csrf.CsrfViewMiddleware' in settings.MIDDLEWARE:
        print("✅ CSRF защита включена")
    else:
        issues.append("❌ CSRF защита отключена!")
    
    # 6. Проверка XSS защиты
    if settings.SECURE_BROWSER_XSS_FILTER:
        print("✅ XSS защита включена")
    else:
        warnings.append("⚠️ XSS защита отключена")
    
    # 7. Проверка Content Security Policy
    if hasattr(settings, 'CSP_DEFAULT_SRC'):
        print("✅ Content Security Policy настроен")
    else:
        warnings.append("⚠️ Content Security Policy не настроен")
    
    return issues, warnings

def check_code_security():
    """Проверяет безопасность кода"""
    print("\n🔍 ПРОВЕРКА БЕЗОПАСНОСТИ КОДА")
    print("=" * 50)
    
    issues = []
    warnings = []
    
    # Ищем потенциально опасные конструкции
    dangerous_patterns = [
        (r'\.raw\(', 'Raw SQL запросы'),
        (r'\.extra\(', 'Extra SQL запросы'),
        (r'cursor\.execute\(', 'Прямые SQL запросы'),
        (r'connection\.cursor\(', 'Прямые SQL запросы'),
        (r'%s.*%s', 'Форматирование строк в SQL'),
        (r'\.format\(.*SELECT', 'Форматирование SQL'),
        (r'f".*SELECT', 'F-строки в SQL'),
        (r"f'.*SELECT", 'F-строки в SQL'),
        (r'eval\(', 'Использование eval()'),
        (r'exec\(', 'Использование exec()'),
        (r'__import__\(', 'Динамический импорт'),
        (r'pickle\.loads\(', 'Небезопасная десериализация'),
    ]
    
    python_files = []
    for root, dirs, files in os.walk('.'):
        if 'venv' in root or '__pycache__' in root or '.git' in root:
            continue
        for file in files:
            if file.endswith('.py') and not file.startswith('test_'):
                python_files.append(os.path.join(root, file))
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                for pattern, description in dangerous_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        issues.append(f"❌ {file_path}: {description}")
        except:
            continue
    
    if not issues:
        print("✅ Опасные конструкции не найдены")
    
    return issues, warnings

def check_authentication_security():
    """Проверяет безопасность аутентификации"""
    print("\n🔐 ПРОВЕРКА АУТЕНТИФИКАЦИИ")
    print("=" * 50)
    
    issues = []
    warnings = []
    
    # Проверяем настройки паролей
    if hasattr(settings, 'AUTH_PASSWORD_VALIDATORS'):
        validators = settings.AUTH_PASSWORD_VALIDATORS
        if len(validators) < 3:
            warnings.append("⚠️ Мало валидаторов паролей")
        else:
            print("✅ Валидаторы паролей настроены")
    
    # Проверяем настройки сессий
    if settings.SESSION_COOKIE_AGE > 86400:  # 24 часа
        warnings.append("⚠️ Слишком долгое время жизни сессии")
    else:
        print("✅ Время жизни сессии разумное")
    
    # Проверяем настройки CSRF
    if settings.CSRF_COOKIE_AGE > 86400:  # 24 часа
        warnings.append("⚠️ Слишком долгое время жизни CSRF токена")
    else:
        print("✅ Время жизни CSRF токена разумное")
    
    return issues, warnings

def check_file_upload_security():
    """Проверяет безопасность загрузки файлов"""
    print("\n📁 ПРОВЕРКА ЗАГРУЗКИ ФАЙЛОВ")
    print("=" * 50)
    
    issues = []
    warnings = []
    
    # Проверяем лимиты размера файлов
    if hasattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE'):
        max_size = settings.FILE_UPLOAD_MAX_MEMORY_SIZE
        if max_size > 50 * 1024 * 1024:  # 50MB
            warnings.append("⚠️ Слишком большой лимит размера файла")
        else:
            print("✅ Лимит размера файла разумный")
    
    # Проверяем лимиты количества полей
    if hasattr(settings, 'DATA_UPLOAD_MAX_NUMBER_FIELDS'):
        max_fields = settings.DATA_UPLOAD_MAX_NUMBER_FIELDS
        if max_fields > 1000:
            warnings.append("⚠️ Слишком большой лимит полей формы")
        else:
            print("✅ Лимит полей формы разумный")
    
    return issues, warnings

def check_rate_limiting():
    """Проверяет настройки rate limiting"""
    print("\n⏱️ ПРОВЕРКА RATE LIMITING")
    print("=" * 50)
    
    issues = []
    warnings = []
    
    # Проверяем, используется ли django-ratelimit
    try:
        import django_ratelimit
        print("✅ django-ratelimit установлен")
    except ImportError:
        warnings.append("⚠️ django-ratelimit не установлен")
    
    return issues, warnings

def main():
    """Основная функция проверки"""
    print("🔐 УЛУЧШЕННАЯ ПРОВЕРКА БЕЗОПАСНОСТИ SUPERPAN")
    print("=" * 60)
    
    all_issues = []
    all_warnings = []
    
    # Запускаем все проверки
    issues, warnings = check_security_settings()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_code_security()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_authentication_security()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_file_upload_security()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_rate_limiting()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    # Выводим результаты
    print("\n" + "=" * 60)
    print("📊 ИТОГОВЫЕ РЕЗУЛЬТАТЫ")
    print("=" * 60)
    
    if all_issues:
        print(f"\n❌ КРИТИЧЕСКИЕ ПРОБЛЕМЫ ({len(all_issues)}):")
        for issue in all_issues:
            print(f"   {issue}")
    
    if all_warnings:
        print(f"\n⚠️ ПРЕДУПРЕЖДЕНИЯ ({len(all_warnings)}):")
        for warning in all_warnings:
            print(f"   {warning}")
    
    if not all_issues and not all_warnings:
        print("\n🟢 ОТЛИЧНО: Все проверки безопасности пройдены!")
    elif not all_issues:
        print(f"\n🟡 ХОРОШО: {len(all_warnings)} предупреждений, но критических проблем нет")
    else:
        print(f"\n🔴 ТРЕБУЕТ ВНИМАНИЯ: {len(all_issues)} критических проблем, {len(all_warnings)} предупреждений")
    
    # Оценка безопасности
    total_checks = 20  # Примерное количество проверок
    passed_checks = total_checks - len(all_issues) - len(all_warnings) // 2
    
    security_score = (passed_checks / total_checks) * 100
    print(f"\n📈 ОЦЕНКА БЕЗОПАСНОСТИ: {security_score:.1f}%")
    
    if security_score >= 90:
        print("🟢 ОТЛИЧНЫЙ УРОВЕНЬ БЕЗОПАСНОСТИ")
    elif security_score >= 75:
        print("🟡 ХОРОШИЙ УРОВЕНЬ БЕЗОПАСНОСТИ")
    elif security_score >= 60:
        print("🟠 УДОВЛЕТВОРИТЕЛЬНЫЙ УРОВЕНЬ БЕЗОПАСНОСТИ")
    else:
        print("🔴 НИЗКИЙ УРОВЕНЬ БЕЗОПАСНОСТИ")
    
    return len(all_issues) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

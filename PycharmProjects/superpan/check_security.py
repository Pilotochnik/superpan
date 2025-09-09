#!/usr/bin/env python
"""
🔐 Скрипт проверки безопасности SuperPan
Проверяет критические настройки безопасности
"""
import os
import sys
import django
from pathlib import Path

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
        issues.append("❌ DEBUG=True - отключите в продакшене!")
    else:
        print("✅ DEBUG=False")
    
    # 2. Проверка SECRET_KEY
    if settings.SECRET_KEY == 'django-insecure-change-this-in-production':
        issues.append("❌ SECRET_KEY не изменен - используйте случайный ключ!")
    else:
        print("✅ SECRET_KEY настроен")
    
    # 3. Проверка ALLOWED_HOSTS
    if '*' in settings.ALLOWED_HOSTS:
        issues.append("❌ ALLOWED_HOSTS содержит '*' - ограничьте домены!")
    else:
        print("✅ ALLOWED_HOSTS настроен безопасно")
    
    # 4. Проверка HTTPS настроек
    if not settings.SECURE_SSL_REDIRECT and not settings.DEBUG:
        warnings.append("⚠️ SECURE_SSL_REDIRECT=False - включите для продакшена")
    else:
        print("✅ SECURE_SSL_REDIRECT настроен")
    
    # 5. Проверка cookie настроек
    if not settings.SESSION_COOKIE_SECURE and not settings.DEBUG:
        warnings.append("⚠️ SESSION_COOKIE_SECURE=False - включите для HTTPS")
    else:
        print("✅ SESSION_COOKIE_SECURE настроен")
    
    if not settings.CSRF_COOKIE_SECURE and not settings.DEBUG:
        warnings.append("⚠️ CSRF_COOKIE_SECURE=False - включите для HTTPS")
    else:
        print("✅ CSRF_COOKIE_SECURE настроен")
    
    # 6. Проверка заголовков безопасности
    security_headers = [
        'SECURE_BROWSER_XSS_FILTER',
        'SECURE_CONTENT_TYPE_NOSNIFF',
        'X_FRAME_OPTIONS',
    ]
    
    for header in security_headers:
        if hasattr(settings, header):
            print(f"✅ {header} настроен")
        else:
            warnings.append(f"⚠️ {header} не настроен")
    
    # 7. Проверка базы данных
    if 'sqlite' in settings.DATABASES['default']['ENGINE'] and not settings.DEBUG:
        warnings.append("⚠️ Используется SQLite - рассмотрите PostgreSQL для продакшена")
    else:
        print("✅ База данных настроена")
    
    # Вывод результатов
    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТЫ ПРОВЕРКИ")
    print("=" * 50)
    
    if issues:
        print("\n🚨 КРИТИЧНЫЕ ПРОБЛЕМЫ:")
        for issue in issues:
            print(f"   {issue}")
    
    if warnings:
        print("\n⚠️ ПРЕДУПРЕЖДЕНИЯ:")
        for warning in warnings:
            print(f"   {warning}")
    
    if not issues and not warnings:
        print("\n🎉 Все настройки безопасности в порядке!")
    
    # Общая оценка
    total_checks = len(security_headers) + 6  # 6 основных проверок
    passed_checks = total_checks - len(issues) - len(warnings)
    score = (passed_checks / total_checks) * 100
    
    print(f"\n📈 Оценка безопасности: {score:.1f}%")
    
    if score >= 90:
        print("🟢 Отличная безопасность!")
    elif score >= 70:
        print("🟡 Хорошая безопасность, есть что улучшить")
    else:
        print("🔴 Требуется серьезная работа над безопасностью")
    
    return len(issues) == 0

def check_dependencies():
    """Проверяет установленные зависимости"""
    print("\n📦 ПРОВЕРКА ЗАВИСИМОСТЕЙ")
    print("=" * 30)
    
    required_packages = [
        'django',
        'django-ratelimit',
        'django-cors-headers',
        'cryptography',
        'Pillow',
        'python-decouple',
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - не установлен")
    
    if missing_packages:
        print(f"\n⚠️ Установите недостающие пакеты:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def main():
    """Основная функция"""
    print("🔐 ПРОВЕРКА БЕЗОПАСНОСТИ SUPERPAN")
    print("=" * 50)
    
    # Проверяем зависимости
    deps_ok = check_dependencies()
    
    # Проверяем настройки безопасности
    security_ok = check_security_settings()
    
    print("\n" + "=" * 50)
    if deps_ok and security_ok:
        print("🎉 Все проверки пройдены успешно!")
        return 0
    else:
        print("❌ Обнаружены проблемы, требующие внимания")
        return 1

if __name__ == "__main__":
    sys.exit(main())

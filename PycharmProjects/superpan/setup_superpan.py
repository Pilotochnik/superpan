#!/usr/bin/env python
"""
🚀 Скрипт для быстрого запуска системы "Проектный Офис"
Автоматически настраивает и запускает систему управления строительными проектами
"""
import os
import sys
import subprocess
import time

def print_header():
    """Выводит заголовок"""
    print("=" * 80)
    print("🏗️  ПРОЕКТНЫЙ ОФИС - СИСТЕМА УПРАВЛЕНИЯ СТРОИТЕЛЬНЫМИ ПРОЕКТАМИ  🏗️")
    print("=" * 80)
    print()

def check_python():
    """Проверяет версию Python"""
    print("🐍 Проверка Python...")
    if sys.version_info < (3, 8):
        print("❌ Требуется Python 3.8 или выше")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} найден")

def setup_virtualenv():
    """Настраивает виртуальное окружение"""
    print("\n📦 Настройка виртуального окружения...")
    
    if not os.path.exists('venv'):
        print("Создание виртуального окружения...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
        print("✅ Виртуальное окружение создано")
    else:
        print("✅ Виртуальное окружение уже существует")

def get_python_path():
    """Возвращает путь к Python в виртуальном окружении"""
    if os.name == 'nt':  # Windows
        return os.path.join('venv', 'Scripts', 'python.exe')
    else:  # Linux/Mac
        return os.path.join('venv', 'bin', 'python')

def install_requirements():
    """Устанавливает зависимости"""
    print("\n📋 Установка зависимостей...")
    python_path = get_python_path()
    
    try:
        subprocess.run([python_path, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True, text=True)
        print("✅ Зависимости установлены")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка установки зависимостей: {e}")
        print("Попробуйте установить вручную: pip install -r requirements.txt")
        return False
    return True

def setup_database():
    """Настраивает базу данных"""
    print("\n🗄️ Настройка базы данных...")
    python_path = get_python_path()
    
    # Миграции
    try:
        subprocess.run([python_path, 'manage.py', 'makemigrations'], check=True)
        subprocess.run([python_path, 'manage.py', 'migrate'], check=True)
        print("✅ База данных настроена")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка настройки БД: {e}")
        return False
    return True

def create_superuser():
    """Создает суперпользователя"""
    print("\n👑 Создание суперпользователя...")
    python_path = get_python_path()
    
    try:
        subprocess.run([python_path, 'manage.py', 'create_demo_superuser'], check=True)
        print("✅ Суперпользователь создан")
    except subprocess.CalledProcessError:
        print("ℹ️ Суперпользователь уже существует или произошла ошибка")
    return True

def create_demo_data():
    """Создает демо-данные"""
    print("\n🎯 Создание демо-данных...")
    python_path = get_python_path()
    
    try:
        subprocess.run([python_path, 'manage.py', 'create_demo_data'], check=True)
        print("✅ Демо-данные созданы")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Демо-данные не созданы: {e}")
    return True

def collect_static():
    """Собирает статические файлы"""
    print("\n🎨 Сборка статических файлов...")
    python_path = get_python_path()
    
    try:
        subprocess.run([python_path, 'manage.py', 'collectstatic', '--noinput'], 
                      check=True, capture_output=True)
        print("✅ Статические файлы собраны")
    except subprocess.CalledProcessError:
        print("⚠️ Статические файлы не собраны (не критично)")
    return True

def start_server():
    """Запускает сервер разработки"""
    print("\n🚀 Запуск сервера...")
    python_path = get_python_path()
    
    print("=" * 80)
    print("🎉 Проектный Офис готов к работе!")
    print("=" * 80)
    print()
    print("🌐 Доступные страницы:")
    print("   📊 Главная система: http://127.0.0.1:8000/")
    print("   ⚙️ Простая админка: http://127.0.0.1:8000/management/")
    print("   🔧 Django админка: http://127.0.0.1:8000/admin/")
    print()
    print("👥 Учетные данные:")
    print("   🔑 Администратор: admin@project-office.ru / admin123")
    print("   👷 Прораб: foreman@project-office.ru / foreman123")
    print("   🔨 Подрядчик: contractor1@project-office.ru / contractor123")
    print()
    print("🛑 Для остановки сервера нажмите Ctrl+C")
    print("=" * 80)
    print()
    
    try:
        subprocess.run([python_path, 'manage.py', 'runserver'], check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Сервер остановлен")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Ошибка запуска сервера: {e}")

def main():
    """Основная функция"""
    print_header()
    
    # Проверяем, что мы в правильной директории
    if not os.path.exists('manage.py'):
        print("❌ Файл manage.py не найден. Запустите скрипт из корневой директории проекта.")
        sys.exit(1)
    
    try:
        # Пошаговая настройка
        check_python()
        setup_virtualenv()
        
        if not install_requirements():
            return
            
        if not setup_database():
            return
            
        create_superuser()
        create_demo_data()
        collect_static()
        
        # Небольшая пауза перед запуском сервера
        print("\n⏳ Подготовка к запуску...")
        time.sleep(2)
        
        start_server()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Настройка прервана пользователем")
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")
        print("Попробуйте запустить команды вручную:")
        print("1. python -m venv venv")
        print("2. venv\\Scripts\\activate (Windows) или source venv/bin/activate (Linux/Mac)")
        print("3. pip install -r requirements.txt")
        print("4. python manage.py migrate")
        print("5. python manage.py create_demo_superuser")
        print("6. python manage.py runserver")

if __name__ == "__main__":
    main()

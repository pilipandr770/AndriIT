"""
Скрипт для замены app/__init__.py
"""
import os
import shutil
import sys

def patch_app_init():
    """Заменяет app/__init__.py на версию без импорта flask_admin"""
    try:
        # Проверяем, существует ли новый файл
        if not os.path.exists('app/__init__.py.new'):
            print("Файл app/__init__.py.new не найден")
            return False
        
        # Создаем резервную копию оригинального файла
        if os.path.exists('app/__init__.py'):
            shutil.copy2('app/__init__.py', 'app/__init__.py.bak')
            print("Создана резервная копия app/__init__.py")
        
        # Заменяем оригинальный файл новым
        shutil.copy2('app/__init__.py.new', 'app/__init__.py')
        print("Файл app/__init__.py успешно заменен")
        
        return True
    except Exception as e:
        print(f"Ошибка при замене файла app/__init__.py: {e}")
        return False

if __name__ == "__main__":
    patch_app_init()
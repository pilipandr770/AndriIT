"""
Точка входа для Gunicorn
"""
import sys
import os

# ВАЖНО: Применяем патчи для Python 3.13 ДО импорта SQLAlchemy
if sys.version_info >= (3, 13):
    print(f"Running on Python {sys.version}")
    # Импортируем патчи для совместимости с Python 3.13
    try:
        import python313_patch
        print("Python 3.13 patches applied")
    except ImportError:
        print("Warning: python313_patch not found")
    
    # Отключаем использование greenlet в SQLAlchemy
    try:
        import sqlalchemy_no_greenlet
        print("SQLAlchemy configured to work without greenlet")
    except ImportError:
        print("Warning: sqlalchemy_no_greenlet not found")
    
    # Устанавливаем переменные окружения для совместимости
    os.environ['PYTHONWARNINGS'] = 'ignore::DeprecationWarning'

# Применяем патч для flask_admin
try:
    import app_init_patch
    print("Flask-Admin patch applied")
except ImportError:
    print("Warning: app_init_patch not found")

# Импортируем Flask-Admin перед импортом приложения
try:
    import flask_admin
    print(f"Flask-Admin version: {getattr(flask_admin, '__version__', 'unknown')}")
except ImportError:
    print("Warning: flask_admin not found, trying to install it")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Flask-Admin==1.6.1"])
        import flask_admin
        print(f"Flask-Admin installed and imported: {getattr(flask_admin, '__version__', 'unknown')}")
    except Exception as e:
        print(f"Error installing Flask-Admin: {e}")

# Импортируем и создаем приложение
from run import app

# Экспортируем переменную app для gunicorn
application = app

if __name__ == '__main__':
    app.run(debug=True)
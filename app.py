"""
Точка входа для Gunicorn
"""
import sys
import os

print("Starting app.py")

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

# Применяем патч для app/__init__.py
try:
    import patch_app_init
    patch_app_init.patch_app_init()
    print("app/__init__.py patched")
except ImportError:
    print("Warning: patch_app_init not found")
except Exception as e:
    print(f"Error patching app/__init__.py: {e}")

# Применяем патч для flask_admin
try:
    import app_init_patch
    print("Flask-Admin patch applied")
except ImportError:
    print("Warning: app_init_patch not found")

# Создаем заглушку для flask_admin в sys.modules
if 'flask_admin' not in sys.modules:
    print("Creating mock flask_admin module")
    class MockAdmin:
        def __init__(self, name=None, template_mode=None, **kwargs):
            self.name = name
            self.template_mode = template_mode
            self.kwargs = kwargs
        
        def init_app(self, app):
            return self
    
    # Создаем фиктивный модуль
    import types
    mock_admin = types.ModuleType('flask_admin')
    mock_admin.Admin = MockAdmin
    mock_admin.__version__ = '0.0.0'
    
    # Добавляем в sys.modules
    sys.modules['flask_admin'] = mock_admin
    print("Mock flask_admin module created")

# Импортируем и создаем приложение
try:
    from run import app
    print("Successfully imported app from run.py")
except ImportError as e:
    print(f"Error importing app from run.py: {e}")
    # Создаем минимальное приложение Flask
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return "Hello, World! This is a minimal Flask app."

# Экспортируем переменную app для gunicorn
application = app

if __name__ == '__main__':
    app.run(debug=True)
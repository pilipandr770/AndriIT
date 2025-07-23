"""
Патч для app/__init__.py, который заменяет импорт flask_admin
"""
import os
import sys
import importlib.util
import types

def create_mock_admin():
    """Создает заглушку для Flask-Admin"""
    class MockAdmin:
        def __init__(self, name=None, template_mode=None, **kwargs):
            self.name = name
            self.template_mode = template_mode
            self.kwargs = kwargs
            print(f"Created MockAdmin with name={name}, template_mode={template_mode}")
        
        def init_app(self, app):
            print(f"Initialized MockAdmin for app {app.name}")
            return self
        
        def add_view(self, view):
            print(f"Added view to MockAdmin: {view}")
            return self
    
    # Создаем фиктивный модуль flask_admin
    mock_admin_module = types.ModuleType('flask_admin')
    mock_admin_module.Admin = MockAdmin
    
    # Добавляем необходимые подмодули и классы
    mock_admin_module.form = types.ModuleType('flask_admin.form')
    mock_admin_module.contrib = types.ModuleType('flask_admin.contrib')
    mock_admin_module.contrib.sqla = types.ModuleType('flask_admin.contrib.sqla')
    
    class MockModelView:
        def __init__(self, model, session, **kwargs):
            self.model = model
            self.session = session
            self.kwargs = kwargs
    
    mock_admin_module.contrib.sqla.ModelView = MockModelView
    
    return mock_admin_module

def apply_patch():
    """Применяет патч для app/__init__.py"""
    # Проверяем, установлен ли flask_admin
    try:
        import flask_admin
        print(f"Flask-Admin уже установлен: {flask_admin.__version__}")
        return
    except ImportError:
        print("Flask-Admin не установлен, применяем патч")
    
    # Создаем заглушку для flask_admin
    mock_admin = create_mock_admin()
    
    # Добавляем заглушку в sys.modules
    sys.modules['flask_admin'] = mock_admin
    
    print("Патч для flask_admin успешно применен")

# Применяем патч при импорте модуля
apply_patch()
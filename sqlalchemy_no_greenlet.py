"""
Патч для отключения использования greenlet в SQLAlchemy
Этот файл должен быть импортирован до импорта SQLAlchemy
"""
import os
import sys

# Устанавливаем переменную окружения, чтобы отключить использование greenlet
os.environ["SQLALCHEMY_WARN_20"] = "1"
os.environ["SQLALCHEMY_NO_ASYNC"] = "1"

# Создаем фиктивный модуль greenlet для обхода импорта
class MockGreenlet:
    def __init__(self, *args, **kwargs):
        pass
    
    def switch(self, *args, **kwargs):
        raise NotImplementedError("Greenlet отключен")
    
    @staticmethod
    def getcurrent():
        return None

# Добавляем фиктивный модуль в sys.modules
if "greenlet" not in sys.modules:
    sys.modules["greenlet"] = type("greenlet", (), {
        "greenlet": MockGreenlet,
        "__version__": "0.0.0"
    })

print("SQLAlchemy настроен для работы без greenlet")
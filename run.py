#!/usr/bin/env python
"""
Flask Shop Application
"""
import sys
import os

# ВАЖНО: Применяем патчи для Python 3.13 ДО импорта SQLAlchemy
if sys.version_info >= (3, 13):
    print(f"Running on Python {sys.version}")
    # Импортируем патчи для совместимости с Python 3.13
    import python313_patch
    
    # Устанавливаем переменные окружения для совместимости
    os.environ['PYTHONWARNINGS'] = 'ignore::DeprecationWarning'

# Импортируем и создаем приложение
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
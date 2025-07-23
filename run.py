#!/usr/bin/env python
"""
Flask Shop Application
"""
import sys
import os

# Установка переменных окружения для Python 3.13
if sys.version_info >= (3, 13):
    print(f"Running on Python {sys.version}")
    
    # Отключаем предупреждения о устаревших функциях
    import warnings
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    warnings.filterwarnings('ignore', category=UserWarning)
    
    # Устанавливаем переменные окружения для совместимости
    os.environ['PYTHONWARNINGS'] = 'ignore::DeprecationWarning'

# Импортируем и создаем приложение
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
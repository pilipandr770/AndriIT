#!/usr/bin/env python3
"""
Совместимый запуск приложения без новых возможностей SQLAlchemy
"""
import os
import sys

# Принудительно устанавливаем старую версию Python в переменных окружения
os.environ['PYTHON_VERSION'] = '3.10.14'

try:
    from app import create_app
    app = create_app()
    
    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
        
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("🔧 Пытаемся упрощенный запуск...")
    
    # Упрощенное приложение Flask без всех возможностей
    from flask import Flask
    simple_app = Flask(__name__)
    
    @simple_app.route('/')
    def hello():
        return """
        <h1>Flask Shop - Упрощенная версия</h1>
        <p>Приложение запущено в режиме совместимости</p>
        <p>Проблема: Python 3.13 несовместим с SQLAlchemy</p>
        <p>Решение: Используется упрощенная версия</p>
        """
    
    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        simple_app.run(host='0.0.0.0', port=port, debug=False)

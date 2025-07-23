#!/bin/bash
# Explicit start script for Render
echo "Starting Flask app using app.py"

# Проверяем, что Flask-Admin установлен
pip list | grep Flask-Admin

# Запускаем приложение
gunicorn --bind 0.0.0.0:$PORT app:app --workers 1 --timeout 120
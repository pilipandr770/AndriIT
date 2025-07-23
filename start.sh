#!/bin/bash
# Explicit start script for Render
echo "Starting Flask app using app.py"

# Проверяем, что Flask-Admin установлен
pip list | grep Flask-Admin || echo "Flask-Admin not found in pip list"

# Устанавливаем Flask-Admin явно
pip install Flask-Admin==1.6.1

# Запускаем приложение с явным указанием переменной application
gunicorn --bind 0.0.0.0:$PORT app:application --workers 1 --timeout 120
#!/bin/bash
# Explicit start script for Render
echo "Starting Flask app using app.py"

# Проверяем, что Flask-Admin установлен
pip list | grep Flask-Admin || echo "Flask-Admin not found in pip list"

# Устанавливаем Flask-Admin явно
pip install Flask-Admin==1.6.1

# Копируем app/__init__.py.new в app/__init__.py
if [ -f app/__init__.py.new ]; then
  cp -f app/__init__.py app/__init__.py.bak
  cp -f app/__init__.py.new app/__init__.py
  echo "Replaced app/__init__.py with app/__init__.py.new"
fi

# Запускаем приложение с явным указанием переменной application
echo "Running: gunicorn --bind 0.0.0.0:$PORT app:application --workers 1 --timeout 120"
gunicorn --bind 0.0.0.0:$PORT app:application --workers 1 --timeout 120
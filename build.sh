#!/bin/bash
# Explicit build script for Render
echo "Installing dependencies without greenlet"

# Устанавливаем переменные окружения для отключения greenlet в SQLAlchemy
export SQLALCHEMY_WARN_20=1
export SQLALCHEMY_NO_ASYNC=1

# Устанавливаем зависимости без greenlet
pip install -r requirements_no_greenlet.txt

# Явно устанавливаем Flask-Admin
pip install Flask-Admin==1.6.1

# Запускаем скрипт для установки Flask-Admin
python install_flask_admin.py

# Проверяем, что Flask-Admin установлен
pip list | grep Flask-Admin || echo "Flask-Admin not found in pip list"

# Создаем директорию для резервных копий
mkdir -p backups

# Копируем app/__init__.py.new в app/__init__.py
if [ -f app/__init__.py.new ]; then
  cp -f app/__init__.py app/__init__.py.bak
  cp -f app/__init__.py.new app/__init__.py
  echo "Replaced app/__init__.py with app/__init__.py.new"
fi
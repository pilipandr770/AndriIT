#!/bin/bash
# Simplified build script for Render - no SQLAlchemy
echo "Installing minimal dependencies for Flask-only deployment"

# Install only the minimal requirements needed for Flask
pip install -r requirements_minimal.txt

echo "Python version:"
python --version

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
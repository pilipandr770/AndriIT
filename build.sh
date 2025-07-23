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
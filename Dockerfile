FROM python:3.10.14-slim

WORKDIR /app

# Копируем файлы зависимостей
COPY requirements_legacy.txt .
COPY runtime.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements_legacy.txt

# Копируем приложение
COPY . .

# Открываем порт
EXPOSE $PORT

# Команда запуска
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT run:app --workers 1 --timeout 120"]

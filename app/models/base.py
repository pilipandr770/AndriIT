from app import db
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Получаем строку подключения к базе данных
database_url = os.environ.get('DATABASE_URL', '')
# Получаем имя схемы
schema_name = os.environ.get('DB_SCHEMA', 'AndriIT')

# Определяем аргументы таблицы в зависимости от типа базы данных
if database_url and database_url.startswith('postgresql'):
    TABLE_ARGS = {'schema': schema_name}
else:
    TABLE_ARGS = {}
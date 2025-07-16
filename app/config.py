import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

class Config:
    # Основные настройки Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    DEBUG = os.environ.get('FLASK_DEBUG') == '1'
    
    # Настройки базы данных
    database_url = os.environ.get('DATABASE_URL')
    
    # Исправление для Render PostgreSQL URL (если начинается с postgres://)
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Настройка схемы базы данных
    DB_SCHEMA = os.environ.get('DB_SCHEMA', 'AndriIT')
    
    # Опции для SQLAlchemy для использования указанной схемы
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'options': f'-c search_path={DB_SCHEMA}'
        } if database_url and 'postgresql' in database_url else {}
    }
    
    # Префикс для таблиц в PostgreSQL (схема)
    if database_url and 'postgresql' in database_url:
        SQLALCHEMY_TABLE_ARGS = {'schema': DB_SCHEMA}
    
    # Настройки для загрузки файлов
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    
    # Настройки OpenAI
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_ASSISTANT_ID = os.environ.get('OPENAI_ASSISTANT_ID')
    
    # Настройки Stripe
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
    
    # Настройки Babel для многоязычности
    BABEL_DEFAULT_LOCALE = 'uk'
    BABEL_SUPPORTED_LOCALES = ['uk', 'de', 'en']
    
    # Настройки для админ-панели
    FLASK_ADMIN_SWATCH = 'cerulean'
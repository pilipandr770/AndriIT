#!/usr/bin/env python
"""
Скрипт для инициализации базы данных на Render
"""
import os
from app import create_app, db

def init_database():
    """Инициализация базы данных"""
    app = create_app()
    
    with app.app_context():
        try:
            # Создаем все таблицы
            db.create_all()
            print("✅ База данных успешно инициализирована")
            
            # Создаем схему, если нужно
            db_schema = os.environ.get('DB_SCHEMA', 'AndriIT')
            if db_schema:
                db.engine.execute(f'CREATE SCHEMA IF NOT EXISTS "{db_schema}"')
                print(f"✅ Схема {db_schema} создана")
                
        except Exception as e:
            print(f"❌ Ошибка при инициализации БД: {e}")
            raise

if __name__ == "__main__":
    init_database()

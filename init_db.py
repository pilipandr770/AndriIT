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
            # Создаем схему, если нужно (для SQLAlchemy 1.4)
            db_schema = os.environ.get('DB_SCHEMA', 'AndriIT')
            if db_schema and db_schema != 'public':
                try:
                    db.engine.execute(f'CREATE SCHEMA IF NOT EXISTS "{db_schema}"')
                    print(f"✅ Схема {db_schema} создана")
                except Exception as schema_error:
                    print(f"⚠️ Не удалось создать схему: {schema_error}")
            
            # Создаем все таблицы
            db.create_all()
            print("✅ База данных успешно инициализирована")
                
        except Exception as e:
            print(f"❌ Ошибка при инициализации БД: {e}")
            import traceback
            traceback.print_exc()
            # Не останавливаем развертывание из-за ошибок БД
            print("⚠️ Продолжаем развертывание несмотря на ошибки БД")

if __name__ == "__main__":
    init_database()

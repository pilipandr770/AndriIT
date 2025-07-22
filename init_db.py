#!/usr/bin/env python
"""
Скрипт для инициализации базы данных на Render
"""
import os
from app import create_app, db
from sqlalchemy import text

def init_database():
    """Инициализация базы данных"""
    app = create_app()
    
    with app.app_context():
        try:
            # Создаем схему, если нужно (перед созданием таблиц)
            db_schema = os.environ.get('DB_SCHEMA', 'AndriIT')
            if db_schema and db_schema != 'public':
                with db.engine.connect() as conn:
                    conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{db_schema}"'))
                    conn.commit()
                print(f"✅ Схема {db_schema} создана")
            
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

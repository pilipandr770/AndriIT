import os
import sys
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel
from flask_login import LoginManager
from flask_admin import Admin

# Инициализация расширений
db = SQLAlchemy()
migrate = Migrate()
babel = Babel()
login_manager = LoginManager()
admin = Admin(name="Админ-панель", template_mode="bootstrap4")

def create_app(config_class=None):
    app = Flask(__name__)
    
    # Загрузка конфигурации
    if config_class is None:
        app.config.from_object("app.config.Config")
    else:
        app.config.from_object(config_class)
    
    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    admin.init_app(app)
    
    # Регистрация blueprints
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    
    from app.routes.shop import shop_bp
    app.register_blueprint(shop_bp, url_prefix="/shop")
    
    from app.routes.blog import blog_bp
    app.register_blueprint(blog_bp, url_prefix="/blog")
    
    # Импортируем admin_bp
    from app.routes.admin import admin_bp
    
    # Импортируем маршруты для блога
    from app.routes import blog_admin
    
    # Регистрируем blueprint
    app.register_blueprint(admin_bp, url_prefix="/admin_panel")
    
    from app.chatbot.routes import chatbot_bp
    app.register_blueprint(chatbot_bp)
    
    # Настройка Babel для многоязычности
    def get_locale():
        # Если пользователь выбрал язык, используем его
        if "language" in session:
            return session["language"]
        # Иначе пытаемся определить язык из заголовков запроса
        return request.accept_languages.best_match(["uk", "de", "en"])
    
    babel.init_app(app, locale_selector=get_locale)
    
    # Добавляем глобальные переменные для всех шаблонов
    @app.context_processor
    def inject_globals():
        from datetime import datetime
        
        # Проверяем, существует ли таблица social_links
        has_social_links = False
        try:
            has_social_links = db.inspect(db.engine).has_table("social_links", schema=app.config.get("DB_SCHEMA"))
        except:
            pass
        
        social_links = []
        if has_social_links:
            from app.models.settings import SocialLink
            social_links = SocialLink.query.filter_by(is_active=True).order_by(SocialLink.order).all()
        
        return {
            "now": datetime.now(),
            "social_links": social_links
        }
    
    # Создание схемы и таблиц базы данных
    with app.app_context():
        # Создаем схему, если используется PostgreSQL
        if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgresql"):
            schema_name = app.config.get("DB_SCHEMA", "AndriIT")
            # Выполняем SQL-запрос для создания схемы
            from sqlalchemy import text
            db.session.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"'))
            db.session.commit()
            print(f"Schema '{schema_name}' created or already exists.")
        
        # Создаем таблицы
        db.create_all()
    
    return app



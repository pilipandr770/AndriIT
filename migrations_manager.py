from flask import Flask
from flask.cli import FlaskGroup
from app import create_app, db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

cli = FlaskGroup(create_app=lambda: app)

@cli.command("create_tables")
def create_tables():
    """Создает схему и таблицы базы данных."""
    # Создаем схему, если используется PostgreSQL
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgresql'):
        schema_name = app.config.get('DB_SCHEMA', 'AndriIT')
        # Выполняем SQL-запрос для создания схемы
        db.session.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"')
        db.session.commit()
        print(f"Schema '{schema_name}' created or already exists.")
    
    # Создаем таблицы
    db.create_all()
    print("Таблицы базы данных созданы.")

@cli.command("create_admin")
def create_admin():
    """Создает администратора."""
    from app.models.user import User
    
    username = input("Введите имя пользователя: ")
    email = input("Введите email: ")
    password = input("Введите пароль: ")
    
    user = User.query.filter_by(email=email).first()
    
    if user:
        print(f"Пользователь с email {email} уже существует.")
        make_admin = input("Сделать этого пользователя администратором? (y/n): ")
        if make_admin.lower() == 'y':
            user.is_admin = True
            db.session.commit()
            print(f"Пользователь {email} теперь администратор.")
    else:
        user = User(username=username, email=email, is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"Администратор {username} ({email}) успешно создан.")

if __name__ == '__main__':
    cli()
from app import create_app, db
from app.models.user import User

def make_admin(email):
    """Делает пользователя с указанным email администратором"""
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        
        if not user:
            print(f"Пользователь с email {email} не найден.")
            return False
        
        user.is_admin = True
        db.session.commit()
        print(f"Пользователь {user.username} ({email}) теперь администратор.")
        return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        email = sys.argv[1]
    else:
        email = input("Введите email пользователя, которого нужно сделать администратором: ")
    
    make_admin(email)
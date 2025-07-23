"""
Скрипт для установки Flask-Admin
"""
import subprocess
import sys

def install_flask_admin():
    print("Устанавливаем Flask-Admin...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Flask-Admin==1.6.1"])
        print("Flask-Admin успешно установлен!")
        return True
    except Exception as e:
        print(f"Ошибка при установке Flask-Admin: {e}")
        return False

if __name__ == "__main__":
    install_flask_admin()
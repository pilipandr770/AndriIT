"""
WSGI entry point for Gunicorn
"""
from run import app

if __name__ == "__main__":
    app.run()
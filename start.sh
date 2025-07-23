#!/bin/bash
# Simplified start script for Render.com - No SQLAlchemy
echo "Starting Flask app using app_direct.py (SQLAlchemy-free version)"

# Show Python version
python --version

# Show environment variables (excluding secrets)
echo "PORT: $PORT"
echo "PYTHONPATH: $PYTHONPATH"

# Start the application using gunicorn
exec gunicorn app_direct:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
fi

# Запускаем приложение с явным указанием переменной application
echo "Running: gunicorn --bind 0.0.0.0:$PORT app:application --workers 1 --timeout 120"
gunicorn --bind 0.0.0.0:$PORT app:application --workers 1 --timeout 120
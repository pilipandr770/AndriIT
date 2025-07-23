#!/bin/sh
# Simple direct startup script that doesn't rely on Docker
# To be used if Docker deployment fails

pip install -r requirements.txt gunicorn

# Start the application using fixed port 10000
exec gunicorn --bind 0.0.0.0:10000 --workers 1 --threads 8 --timeout 120 run:app

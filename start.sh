#!/bin/bash
# Explicit start script for Render
echo "Starting Flask app using wsgi.py"
gunicorn --bind 0.0.0.0:$PORT wsgi:app --workers 1 --timeout 120
#!/bin/bash
# Explicit start script for Render
echo "Starting Flask app"
gunicorn --bind 0.0.0.0:$PORT run:app --workers 1 --timeout 120
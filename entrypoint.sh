#!/bin/bash
set -e

# Default to port 8080 if PORT not set
PORT="${PORT:-8080}"

echo "Starting server on port $PORT"
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 120 run:app

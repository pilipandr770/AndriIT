#!/bin/bash
# Explicit start script for Render
echo "Starting ultra minimal Flask app"
gunicorn ultra_minimal_app:app
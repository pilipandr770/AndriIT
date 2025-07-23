#!/usr/bin/env python
"""
Deploy script for existing Flask Shop application
"""
import os

# Import the existing app
from app import create_app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug, host='0.0.0.0', port=port)

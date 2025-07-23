#!/usr/bin/env python
"""
Minimal Flask application for deployment on Render with Python 3.13
This version avoids using SQLAlchemy and other problematic dependencies
"""
import os
import sys
from flask import Flask, jsonify, render_template, redirect, url_for, request

# Create Flask application
app = Flask(__name__)

# Load configuration from environment variables
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', '0') == '1'

# Basic routes
@app.route('/')
def index():
    """Main page route"""
    return render_template('main/index.html', 
                          title="Flask Shop - Интернет-магазин",
                          year=2025)

@app.route('/about')
def about():
    """About page route"""
    return render_template('main/page.html', 
                          title="О нас - Flask Shop",
                          content="Информация о нашем магазине",
                          year=2025)

@app.route('/contact')
def contact():
    """Contact page route"""
    return render_template('main/contact.html',
                          title="Контакты - Flask Shop",
                          year=2025)

@app.route('/privacy')
def privacy():
    """Privacy policy page route"""
    return render_template('main/privacy.html',
                          title="Политика конфиденциальности - Flask Shop",
                          year=2025)

@app.route('/terms')
def terms():
    """Terms page route"""
    return render_template('main/terms.html',
                          title="Условия использования - Flask Shop",
                          year=2025)

@app.route('/impressum')
def impressum():
    """Impressum page route"""
    return render_template('main/impressum.html',
                          title="Impressum - Flask Shop",
                          year=2025)

# API endpoints
@app.route('/api/status')
def api_status():
    """API status endpoint"""
    return jsonify({
        'status': 'running',
        'version': '1.0-minimal',
        'python_version': sys.version,
        'mode': 'minimal_mode',
        'env': os.environ.get('FLASK_ENV', 'production')
    })

@app.route('/set_language/<lang>')
def set_language(lang):
    """Set language route"""
    # In minimal mode, we don't actually change language
    # Just redirect back to the previous page or home
    return redirect(request.referrer or url_for('index'))

# This allows the app to be imported by gunicorn
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
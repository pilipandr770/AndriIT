#!/usr/bin/env python
"""
Ultra Minimal Flask application for deployment on Render with Python 3.13
This version uses only Flask and its core dependencies
"""
import os
import sys
from flask import Flask, jsonify, render_template_string, redirect, url_for, request

# Create Flask application
app = Flask(__name__)

# Load configuration from environment variables
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', '0') == '1'

# Basic HTML template
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { background-color: #f8f9fa; padding: 10px 0; margin-bottom: 20px; }
        nav { display: flex; justify-content: space-between; }
        nav ul { list-style: none; display: flex; gap: 20px; }
        nav a { text-decoration: none; color: #333; }
        footer { margin-top: 50px; padding: 20px 0; border-top: 1px solid #eee; }
        .content { min-height: 400px; }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <nav>
                <div>
                    <h1>Flask Shop</h1>
                </div>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/about">About</a></li>
                    <li><a href="/contact">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>
    
    <div class="container">
        <div class="content">
            <h2>{{ title }}</h2>
            {{ content|safe }}
        </div>
    </div>
    
    <footer>
        <div class="container">
            <p>&copy; {{ year }} Flask Shop. All rights reserved.</p>
            <p>
                <a href="/privacy">Privacy Policy</a> | 
                <a href="/terms">Terms of Service</a> | 
                <a href="/impressum">Impressum</a>
            </p>
        </div>
    </footer>
</body>
</html>
"""

# Basic routes
@app.route('/')
def index():
    """Main page route"""
    content = """
    <h3>Welcome to Flask Shop</h3>
    <p>This is a minimal version of the Flask Shop application.</p>
    <p>The site is currently in maintenance mode.</p>
    <p>Please check back later for the full version.</p>
    """
    return render_template_string(BASE_TEMPLATE, 
                                 title="Flask Shop - Интернет-магазин",
                                 content=content,
                                 year=2025)

@app.route('/about')
def about():
    """About page route"""
    content = """
    <h3>About Flask Shop</h3>
    <p>Flask Shop is an e-commerce platform built with Flask.</p>
    <p>The site is currently in maintenance mode.</p>
    """
    return render_template_string(BASE_TEMPLATE, 
                                 title="О нас - Flask Shop",
                                 content=content,
                                 year=2025)

@app.route('/contact')
def contact():
    """Contact page route"""
    content = """
    <h3>Contact Us</h3>
    <p>Email: contact@example.com</p>
    <p>Phone: +1 234 567 890</p>
    <p>The site is currently in maintenance mode.</p>
    """
    return render_template_string(BASE_TEMPLATE,
                                 title="Контакты - Flask Shop",
                                 content=content,
                                 year=2025)

@app.route('/privacy')
def privacy():
    """Privacy policy page route"""
    content = """
    <h3>Privacy Policy</h3>
    <p>This is a placeholder for the privacy policy.</p>
    <p>The site is currently in maintenance mode.</p>
    """
    return render_template_string(BASE_TEMPLATE,
                                 title="Политика конфиденциальности - Flask Shop",
                                 content=content,
                                 year=2025)

@app.route('/terms')
def terms():
    """Terms page route"""
    content = """
    <h3>Terms of Service</h3>
    <p>This is a placeholder for the terms of service.</p>
    <p>The site is currently in maintenance mode.</p>
    """
    return render_template_string(BASE_TEMPLATE,
                                 title="Условия использования - Flask Shop",
                                 content=content,
                                 year=2025)

@app.route('/impressum')
def impressum():
    """Impressum page route"""
    content = """
    <h3>Impressum</h3>
    <p>This is a placeholder for the impressum.</p>
    <p>The site is currently in maintenance mode.</p>
    """
    return render_template_string(BASE_TEMPLATE,
                                 title="Impressum - Flask Shop",
                                 content=content,
                                 year=2025)

# API endpoints
@app.route('/api/status')
def api_status():
    """API status endpoint"""
    return jsonify({
        'status': 'running',
        'version': '1.0-ultra-minimal',
        'python_version': sys.version,
        'mode': 'maintenance_mode',
        'env': os.environ.get('FLASK_ENV', 'production')
    })

# This allows the app to be imported by gunicorn
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
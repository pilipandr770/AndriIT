#!/usr/bin/env python
"""
Simplified Flask application for deployment on Render.com with Python 3.13
This version avoids SQLAlchemy dependencies
"""
from flask import Flask, render_template, jsonify
import os
import sys
from datetime import datetime

app = Flask(__name__,
           template_folder="templates",
           static_folder="static")

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-123')

@app.route('/')
def index():
    return render_template('index.html', 
                          title="Flask Shop - Интернет-магазин",
                          year=datetime.now().year)

@app.route('/about')
def about():
    return render_template('about.html', 
                          title="О нас - Flask Shop",
                          year=datetime.now().year)

@app.route('/contact')
def contact():
    return render_template('contact.html',
                          title="Контакты - Flask Shop",
                          year=datetime.now().year)

@app.route('/api/status')
def api_status():
    return jsonify({
        'status': 'running',
        'version': '1.0-direct',
        'python_version': sys.version,
        'mode': 'no_database',
        'env': os.environ.get('FLASK_ENV', 'production')
    })

@app.errorhandler(404)
def page_not_found(e):
    return render_template('main/404.html', title='404 - Page Not Found', year=datetime.now().year), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('main/500.html', title='500 - Server Error', year=datetime.now().year), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug, host='0.0.0.0', port=port)

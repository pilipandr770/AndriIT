#!/usr/bin/env python
"""
Минимальное приложение без SQLAlchemy для тестирования на Render
"""
from flask import Flask, jsonify, render_template_string
import os

def create_minimal_app():
    """Создает минимальное приложение без базы данных"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-123')
    
    @app.route('/')
    def home():
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Flask Shop - Loading...</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; text-align: center; }
                .container { max-width: 600px; margin: 0 auto; }
                .status { color: #28a745; }
                .info { color: #6c757d; margin-top: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🛍️ Flask Shop</h1>
                <p class="status">✅ Application is running successfully!</p>
                <p class="info">The full application is being prepared...</p>
                <p class="info">Python version: {{ python_version }}</p>
                <p class="info">Environment: {{ environment }}</p>
            </div>
        </body>
        </html>
        '''
        import sys
        return render_template_string(html, 
                                    python_version=sys.version,
                                    environment=os.environ.get('FLASK_ENV', 'development'))
    
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'service': 'flask-shop-minimal',
            'python_version': os.sys.version,
            'environment': os.environ.get('FLASK_ENV', 'development')
        })
    
    @app.route('/api/status')
    def api_status():
        return jsonify({
            'status': 'running',
            'message': 'Minimal Flask Shop API is operational',
            'features': ['health_check', 'status_page'],
            'database': 'not_connected',
            'version': '1.0-minimal'
        })
    
    return app

# Создаем экземпляр приложения
app = create_minimal_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

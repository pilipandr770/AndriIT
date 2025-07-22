#!/usr/bin/env python
"""
Простая заглушка для Flask приложения
"""
from flask import Flask, jsonify

def create_simple_app():
    """Создает простое Flask приложение"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'simple-app-key'
    
    @app.route('/')
    def home():
        return jsonify({
            'status': 'ok',
            'message': 'Flask Shop is starting up...',
            'note': 'This is a fallback version'
        })
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'})
    
    return app

# Создаем экземпляр приложения
app = create_simple_app()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

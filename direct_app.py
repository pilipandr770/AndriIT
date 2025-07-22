#!/usr/bin/env python
"""
Flask Shop Application - Direct Version
Версия магазина без ORM SQLAlchemy для совместимости с Python 3.13
"""
from flask import Flask, render_template, redirect, url_for, flash, session, request, jsonify
import os
import sys
from datetime import datetime

def create_app():
    """Create Flask application with routes but without SQLAlchemy"""
    app = Flask(__name__, 
                template_folder="app/templates",
                static_folder="app/static")
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-123')
    
    # Main routes
    @app.route('/')
    def index():
        return render_template('main/index.html', 
                              title="Flask Shop - Интернет-магазин",
                              year=datetime.now().year)
    
    @app.route('/about')
    def about():
        return render_template('main/about.html', 
                              title="О нас - Flask Shop",
                              year=datetime.now().year)
    
    @app.route('/contact')
    def contact():
        return render_template('main/contact.html',
                              title="Контакты - Flask Shop",
                              year=datetime.now().year)
    
    # Shop routes with dummy data
    @app.route('/shop')
    def shop():
        products = [
            {"id": 1, "name": "Товар 1", "price": 100, "image": "product1.jpg", "description": "Описание товара 1"},
            {"id": 2, "name": "Товар 2", "price": 200, "image": "product2.jpg", "description": "Описание товара 2"},
            {"id": 3, "name": "Товар 3", "price": 300, "image": "product3.jpg", "description": "Описание товара 3"}
        ]
        return render_template('shop/index.html', 
                              products=products,
                              title="Магазин - Flask Shop",
                              year=datetime.now().year)
    
    @app.route('/shop/product/<int:product_id>')
    def product(product_id):
        # Dummy product data
        product = {"id": product_id, "name": f"Товар {product_id}", "price": 100 * product_id, 
                  "image": f"product{product_id}.jpg", 
                  "description": f"Подробное описание товара {product_id}"}
        
        return render_template('shop/product.html', 
                              product=product,
                              title=f"{product['name']} - Flask Shop",
                              year=datetime.now().year)
    
    # Auth routes (simplified)
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            flash('Вход успешно выполнен', 'success')
            return redirect(url_for('index'))
            
        return render_template('auth/login.html',
                              title="Вход - Flask Shop",
                              year=datetime.now().year)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            flash('Регистрация успешно завершена', 'success')
            return redirect(url_for('login'))
            
        return render_template('auth/register.html',
                              title="Регистрация - Flask Shop",
                              year=datetime.now().year)
    
    # API endpoints
    @app.route('/api/products')
    def api_products():
        products = [
            {"id": 1, "name": "Товар 1", "price": 100},
            {"id": 2, "name": "Товар 2", "price": 200},
            {"id": 3, "name": "Товар 3", "price": 300}
        ]
        return jsonify(products)
    
    @app.route('/api/status')
    def api_status():
        return jsonify({
            'status': 'running',
            'version': '1.0-direct',
            'python_version': sys.version,
            'mode': 'no_database',
            'env': os.environ.get('FLASK_ENV', 'production')
        })
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('main/404.html'), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return render_template('main/500.html'), 500
    
    return app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug, host='0.0.0.0', port=port)

from flask import Flask, render_template, redirect, url_for, flash, session, jsonify, request, current_app, Blueprint
import os
import sys

def create_routes():
    """Create main routes blueprint for the application"""
    main_bp = Blueprint('main', __name__)
    
    @main_bp.route('/')
    def index():
        return render_template('main/index.html')
    
    @main_bp.route('/about')
    def about():
        return render_template('main/about.html')
        
    @main_bp.route('/contact')
    def contact():
        return render_template('main/contact.html')
    
    return main_bp

def create_app():
    """Create a Flask application without SQLAlchemy dependencies"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-123')
    
    # Register routes
    from app.routes.main import create_routes as main_routes
    app.register_blueprint(main_routes())
    
    return app

# For direct execution
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

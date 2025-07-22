from datetime import datetime
from app import db

from app.models.base import TABLE_ARGS

class Category(db.Model):
    __tablename__ = 'categories'
    __table_args__ = TABLE_ARGS
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Поля для многоязычности
    name_uk = db.Column(db.String(100))
    name_de = db.Column(db.String(100))
    name_en = db.Column(db.String(100))
    description_uk = db.Column(db.Text)
    description_de = db.Column(db.Text)
    description_en = db.Column(db.Text)
    
    # Отношения
    products = db.relationship('Product', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    __tablename__ = 'products'
    __table_args__ = TABLE_ARGS
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))
    stock = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('AndriIT.categories.id' if TABLE_ARGS else 'categories.id'))
    
    # Поля для многоязычности
    name_uk = db.Column(db.String(100))
    name_de = db.Column(db.String(100))
    name_en = db.Column(db.String(100))
    description_uk = db.Column(db.Text)
    description_de = db.Column(db.Text)
    description_en = db.Column(db.Text)
    
    # Отношения
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    
    def __repr__(self):
        return f'<Product {self.name}>'
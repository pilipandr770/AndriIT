from datetime import datetime
from app import db

from app.models.base import TABLE_ARGS

class Order(db.Model):
    __tablename__ = 'orders'
    __table_args__ = TABLE_ARGS
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('AndriIT.users.id' if TABLE_ARGS else 'users.id'))
    status = db.Column(db.String(20), default='pending')  # pending, paid, shipped, delivered, cancelled
    total_amount = db.Column(db.Float, nullable=False)
    payment_id = db.Column(db.String(100))
    shipping_address = db.Column(db.Text)
    billing_address = db.Column(db.Text)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Отношения
    items = db.relationship('OrderItem', backref='order', lazy='dynamic')
    
    def __repr__(self):
        return f'<Order {self.id}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    __table_args__ = TABLE_ARGS
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('AndriIT.orders.id' if TABLE_ARGS else 'orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('AndriIT.products.id' if TABLE_ARGS else 'products.id'))
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<OrderItem {self.id}>'
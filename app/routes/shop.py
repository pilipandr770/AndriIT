from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify, flash
from flask_login import current_user, login_required
from app import db
from app.models.product import Category, Product
from app.models.order import Order, OrderItem
import stripe
from app.config import Config

shop_bp = Blueprint('shop', __name__)

# Настройка Stripe
stripe.api_key = Config.STRIPE_SECRET_KEY

@shop_bp.route('/')
def index():
    categories = Category.query.all()
    return render_template('shop/index.html', categories=categories)

@shop_bp.route('/category/<slug>')
def category(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    products = Product.query.filter_by(category_id=category.id, is_active=True).all()
    return render_template('shop/category.html', category=category, products=products)

@shop_bp.route('/product/<slug>')
def product(slug):
    product = Product.query.filter_by(slug=slug, is_active=True).first_or_404()
    related_products = Product.query.filter_by(category_id=product.category_id, is_active=True).filter(Product.id != product.id).limit(4).all()
    return render_template('shop/product.html', product=product, related_products=related_products)

@shop_bp.route('/cart')
def cart():
    # Получаем корзину из сессии
    cart_items = session.get('cart', {})
    products = []
    total = 0
    
    # Получаем информацию о товарах
    for product_id, quantity in cart_items.items():
        product = Product.query.get(int(product_id))
        if product and product.is_active:
            item_total = product.price * quantity
            products.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'total': item_total,
                'image': product.image
            })
            total += item_total
    
    return render_template('shop/cart.html', products=products, total=total)

@shop_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    # Проверяем наличие товара на складе
    if product.stock < quantity:
        flash('Извините, недостаточно товара на складе.')
        return redirect(url_for('shop.product', slug=product.slug))
    
    # Получаем текущую корзину или создаем новую
    cart = session.get('cart', {})
    
    # Добавляем товар в корзину или увеличиваем количество
    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity
    
    # Сохраняем корзину в сессии
    session['cart'] = cart
    flash('Товар добавлен в корзину.')
    
    return redirect(url_for('shop.cart'))

@shop_bp.route('/update_cart', methods=['POST'])
def update_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 0))
    
    cart = session.get('cart', {})
    
    if product_id in cart:
        if quantity > 0:
            cart[product_id] = quantity
        else:
            del cart[product_id]
    
    session['cart'] = cart
    return redirect(url_for('shop.cart'))

@shop_bp.route('/remove_from_cart/<product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    
    if product_id in cart:
        del cart[product_id]
        session['cart'] = cart
    
    return redirect(url_for('shop.cart'))

@shop_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = session.get('cart', {})
    
    if not cart_items:
        flash('Ваша корзина пуста.')
        return redirect(url_for('shop.cart'))
    
    if request.method == 'POST':
        # Создаем заказ
        order = Order(
            user_id=current_user.id if current_user.is_authenticated else None,
            status='pending',
            total_amount=0,
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            shipping_address=request.form.get('shipping_address'),
            billing_address=request.form.get('billing_address')
        )
        
        db.session.add(order)
        db.session.flush()  # Получаем ID заказа
        
        total_amount = 0
        
        # Добавляем товары в заказ
        for product_id, quantity in cart_items.items():
            product = Product.query.get(int(product_id))
            if product and product.is_active:
                item_total = product.price * quantity
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    price=product.price
                )
                db.session.add(order_item)
                total_amount += item_total
        
        order.total_amount = total_amount
        db.session.commit()
        
        # Создаем сессию оплаты Stripe
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': 'Заказ №' + str(order.id),
                        },
                        'unit_amount': int(total_amount * 100),  # Сумма в центах
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=url_for('shop.payment_success', order_id=order.id, _external=True),
                cancel_url=url_for('shop.payment_cancel', order_id=order.id, _external=True),
            )
            
            # Очищаем корзину
            session['cart'] = {}
            
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            flash('Ошибка при создании платежа: ' + str(e))
            return redirect(url_for('shop.checkout'))
    
    # Получаем информацию о товарах в корзине
    products = []
    total = 0
    
    for product_id, quantity in cart_items.items():
        product = Product.query.get(int(product_id))
        if product and product.is_active:
            item_total = product.price * quantity
            products.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'total': item_total
            })
            total += item_total
    
    return render_template('shop/checkout.html', products=products, total=total)

@shop_bp.route('/payment/success/<int:order_id>')
def payment_success(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = 'paid'
    db.session.commit()
    
    flash('Оплата прошла успешно! Спасибо за ваш заказ.')
    return render_template('shop/payment_success.html', order=order)

@shop_bp.route('/payment/cancel/<int:order_id>')
def payment_cancel(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = 'cancelled'
    db.session.commit()
    
    flash('Оплата была отменена.')
    return redirect(url_for('shop.cart'))
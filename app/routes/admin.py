from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.product import Category, Product
from app.models.blog import BlogPost, BlogCategory, BlogTopic
from app.models.order import Order
from app.models.settings import SocialLink, SiteSettings
from app.routes.blog import generate_blog_post
import os
from werkzeug.utils import secure_filename
from slugify import slugify
import uuid

admin_bp = Blueprint('admin_panel', __name__)

# РџСЂРѕРІРµСЂРєР° РїСЂР°РІ Р°РґРјРёРЅРёСЃС‚СЂР°С‚РѕСЂР°
def admin_required(func):
    @login_required
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            flash('РЈ РІР°СЃ РЅРµС‚ РїСЂР°РІ РґР»СЏ РґРѕСЃС‚СѓРїР° Рє СЌС‚РѕР№ СЃС‚СЂР°РЅРёС†Рµ.')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    decorated_view.__name__ = func.__name__
    return decorated_view

# Р“Р»Р°РІРЅР°СЏ СЃС‚СЂР°РЅРёС†Р° Р°РґРјРёРЅРєРё
@admin_bp.route('/')
@admin_required
def index():
    # РЎС‚Р°С‚РёСЃС‚РёРєР° РґР»СЏ РґР°С€Р±РѕСЂРґР°
    products_count = Product.query.count()
    orders_count = Order.query.count()
    users_count = User.query.count()
    posts_count = BlogPost.query.count()
    
    # РџРѕСЃР»РµРґРЅРёРµ Р·Р°РєР°Р·С‹
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('admin/index.html', 
                          products_count=products_count,
                          orders_count=orders_count,
                          users_count=users_count,
                          posts_count=posts_count,
                          recent_orders=recent_orders)

# РЈРїСЂР°РІР»РµРЅРёРµ РєР°С‚РµРіРѕСЂРёСЏРјРё С‚РѕРІР°СЂРѕРІ
@admin_bp.route('/categories')
@admin_required
def categories():
    categories = Category.query.all()
    return render_template('admin/categories/index.html', categories=categories)

@admin_bp.route('/categories/create', methods=['GET', 'POST'])
@admin_required
def create_category():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        # РњРЅРѕРіРѕСЏР·С‹С‡РЅС‹Рµ РїРѕР»СЏ
        name_uk = request.form.get('name_uk')
        name_de = request.form.get('name_de')
        name_en = request.form.get('name_en')
        description_uk = request.form.get('description_uk')
        description_de = request.form.get('description_de')
        description_en = request.form.get('description_en')
        
        # РЎРѕР·РґР°РµРј slug РёР· РёРјРµРЅРё
        slug = slugify(name)
        
        # РџСЂРѕРІРµСЂСЏРµРј СѓРЅРёРєР°Р»СЊРЅРѕСЃС‚СЊ slug
        if Category.query.filter_by(slug=slug).first():
            slug = f"{slug}-{uuid.uuid4().hex[:6]}"
        
        # РћР±СЂР°Р±РѕС‚РєР° Р·Р°РіСЂСѓР¶РµРЅРЅРѕРіРѕ РёР·РѕР±СЂР°Р¶РµРЅРёСЏ
        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                # Р“РµРЅРµСЂРёСЂСѓРµРј СѓРЅРёРєР°Р»СЊРЅРѕРµ РёРјСЏ С„Р°Р№Р»Р°
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'categories', unique_filename)
                
                # РЎРѕР·РґР°РµРј РґРёСЂРµРєС‚РѕСЂРёСЋ, РµСЃР»Рё РѕРЅР° РЅРµ СЃСѓС‰РµСЃС‚РІСѓРµС‚
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                file.save(file_path)
                image = f"uploads/categories/{unique_filename}"
        
        # РЎРѕР·РґР°РµРј РЅРѕРІСѓСЋ РєР°С‚РµРіРѕСЂРёСЋ
        category = Category(
            name=name,
            slug=slug,
            description=description,
            image=image,
            name_uk=name_uk,
            name_de=name_de,
            name_en=name_en,
            description_uk=description_uk,
            description_de=description_de,
            description_en=description_en
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash('РљР°С‚РµРіРѕСЂРёСЏ СѓСЃРїРµС€РЅРѕ СЃРѕР·РґР°РЅР°.')
        return redirect(url_for('admin_panel.categories'))
    
    return render_template('admin/categories/create.html')

@admin_bp.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_category(id):
    category = Category.query.get_or_404(id)
    
    if request.method == 'POST':
        category.name = request.form.get('name')
        category.description = request.form.get('description')
        
        # РњРЅРѕРіРѕСЏР·С‹С‡РЅС‹Рµ РїРѕР»СЏ
        category.name_uk = request.form.get('name_uk')
        category.name_de = request.form.get('name_de')
        category.name_en = request.form.get('name_en')
        category.description_uk = request.form.get('description_uk')
        category.description_de = request.form.get('description_de')
        category.description_en = request.form.get('description_en')
        
        # РћР±СЂР°Р±РѕС‚РєР° Р·Р°РіСЂСѓР¶РµРЅРЅРѕРіРѕ РёР·РѕР±СЂР°Р¶РµРЅРёСЏ
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                # Р“РµРЅРµСЂРёСЂСѓРµРј СѓРЅРёРєР°Р»СЊРЅРѕРµ РёРјСЏ С„Р°Р№Р»Р°
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'categories', unique_filename)
                
                # РЎРѕР·РґР°РµРј РґРёСЂРµРєС‚РѕСЂРёСЋ, РµСЃР»Рё РѕРЅР° РЅРµ СЃСѓС‰РµСЃС‚РІСѓРµС‚
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                file.save(file_path)
                
                # РЈРґР°Р»СЏРµРј СЃС‚Р°СЂРѕРµ РёР·РѕР±СЂР°Р¶РµРЅРёРµ, РµСЃР»Рё РѕРЅРѕ СЃСѓС‰РµСЃС‚РІСѓРµС‚
                if category.image:
                    old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], category.image.replace('uploads/', ''))
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                category.image = f"uploads/categories/{unique_filename}"
        
        db.session.commit()
        flash('РљР°С‚РµРіРѕСЂРёСЏ СѓСЃРїРµС€РЅРѕ РѕР±РЅРѕРІР»РµРЅР°.')
        return redirect(url_for('admin_panel.categories'))
    
    return render_template('admin/categories/edit.html', category=category)

@admin_bp.route('/categories/delete/<int:id>', methods=['POST'])
@admin_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    
    # РџСЂРѕРІРµСЂСЏРµРј, РµСЃС‚СЊ Р»Рё С‚РѕРІР°СЂС‹ РІ СЌС‚РѕР№ РєР°С‚РµРіРѕСЂРёРё
    if category.products.count() > 0:
        flash('РќРµРІРѕР·РјРѕР¶РЅРѕ СѓРґР°Р»РёС‚СЊ РєР°С‚РµРіРѕСЂРёСЋ, СЃРѕРґРµСЂР¶Р°С‰СѓСЋ С‚РѕРІР°СЂС‹.')
        return redirect(url_for('admin_panel.categories'))
    
    # РЈРґР°Р»СЏРµРј РёР·РѕР±СЂР°Р¶РµРЅРёРµ, РµСЃР»Рё РѕРЅРѕ СЃСѓС‰РµСЃС‚РІСѓРµС‚
    if category.image:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], category.image.replace('uploads/', ''))
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(category)
    db.session.commit()
    
    flash('РљР°С‚РµРіРѕСЂРёСЏ СѓСЃРїРµС€РЅРѕ СѓРґР°Р»РµРЅР°.')
    return redirect(url_for('admin_panel.categories'))

# РЈРїСЂР°РІР»РµРЅРёРµ С‚РѕРІР°СЂР°РјРё
@admin_bp.route('/products')
@admin_required
def products():
    products = Product.query.all()
    return render_template('admin/products/index.html', products=products)

@admin_bp.route('/products/create', methods=['GET', 'POST'])
@admin_required
def create_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price', 0))
        stock = int(request.form.get('stock', 0))
        category_id = int(request.form.get('category_id'))
        is_active = True if request.form.get('is_active') else False
        
        # РњРЅРѕРіРѕСЏР·С‹С‡РЅС‹Рµ РїРѕР»СЏ
        name_uk = request.form.get('name_uk')
        name_de = request.form.get('name_de')
        name_en = request.form.get('name_en')
        description_uk = request.form.get('description_uk')
        description_de = request.form.get('description_de')
        description_en = request.form.get('description_en')
        
        # РЎРѕР·РґР°РµРј slug РёР· РёРјРµРЅРё
        slug = slugify(name)
        
        # РџСЂРѕРІРµСЂСЏРµРј СѓРЅРёРєР°Р»СЊРЅРѕСЃС‚СЊ slug
        if Product.query.filter_by(slug=slug).first():
            slug = f"{slug}-{uuid.uuid4().hex[:6]}"
        
        # РћР±СЂР°Р±РѕС‚РєР° Р·Р°РіСЂСѓР¶РµРЅРЅРѕРіРѕ РёР·РѕР±СЂР°Р¶РµРЅРёСЏ
        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                # Р“РµРЅРµСЂРёСЂСѓРµРј СѓРЅРёРєР°Р»СЊРЅРѕРµ РёРјСЏ С„Р°Р№Р»Р°
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'products', unique_filename)
                
                # РЎРѕР·РґР°РµРј РґРёСЂРµРєС‚РѕСЂРёСЋ, РµСЃР»Рё РѕРЅР° РЅРµ СЃСѓС‰РµСЃС‚РІСѓРµС‚
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                file.save(file_path)
                image = f"uploads/products/{unique_filename}"
        
        # РЎРѕР·РґР°РµРј РЅРѕРІС‹Р№ С‚РѕРІР°СЂ
        product = Product(
            name=name,
            slug=slug,
            description=description,
            price=price,
            stock=stock,
            category_id=category_id,
            is_active=is_active,
            image=image,
            name_uk=name_uk,
            name_de=name_de,
            name_en=name_en,
            description_uk=description_uk,
            description_de=description_de,
            description_en=description_en
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('РўРѕРІР°СЂ СѓСЃРїРµС€РЅРѕ СЃРѕР·РґР°РЅ.')
        return redirect(url_for('admin_panel.products'))
    
    categories = Category.query.all()
    return render_template('admin/products/create.html', categories=categories)

@admin_bp.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price', 0))
        product.stock = int(request.form.get('stock', 0))
        product.category_id = int(request.form.get('category_id'))
        product.is_active = True if request.form.get('is_active') else False
        
        # РњРЅРѕРіРѕСЏР·С‹С‡РЅС‹Рµ РїРѕР»СЏ
        product.name_uk = request.form.get('name_uk')
        product.name_de = request.form.get('name_de')
        product.name_en = request.form.get('name_en')
        product.description_uk = request.form.get('description_uk')
        product.description_de = request.form.get('description_de')
        product.description_en = request.form.get('description_en')
        
        # РћР±СЂР°Р±РѕС‚РєР° Р·Р°РіСЂСѓР¶РµРЅРЅРѕРіРѕ РёР·РѕР±СЂР°Р¶РµРЅРёСЏ
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                # Р“РµРЅРµСЂРёСЂСѓРµРј СѓРЅРёРєР°Р»СЊРЅРѕРµ РёРјСЏ С„Р°Р№Р»Р°
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'products', unique_filename)
                
                # РЎРѕР·РґР°РµРј РґРёСЂРµРєС‚РѕСЂРёСЋ, РµСЃР»Рё РѕРЅР° РЅРµ СЃСѓС‰РµСЃС‚РІСѓРµС‚
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                file.save(file_path)
                
                # РЈРґР°Р»СЏРµРј СЃС‚Р°СЂРѕРµ РёР·РѕР±СЂР°Р¶РµРЅРёРµ, РµСЃР»Рё РѕРЅРѕ СЃСѓС‰РµСЃС‚РІСѓРµС‚
                if product.image:
                    old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], product.image.replace('uploads/', ''))
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                product.image = f"uploads/products/{unique_filename}"
        
        db.session.commit()
        flash('РўРѕРІР°СЂ СѓСЃРїРµС€РЅРѕ РѕР±РЅРѕРІР»РµРЅ.')
        return redirect(url_for('admin_panel.products'))
    
    categories = Category.query.all()
    return render_template('admin/products/edit.html', product=product, categories=categories)

@admin_bp.route('/products/delete/<int:id>', methods=['POST'])
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    
    # РЈРґР°Р»СЏРµРј РёР·РѕР±СЂР°Р¶РµРЅРёРµ, РµСЃР»Рё РѕРЅРѕ СЃСѓС‰РµСЃС‚РІСѓРµС‚
    if product.image:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], product.image.replace('uploads/', ''))
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(product)
    db.session.commit()
    
    flash('РўРѕРІР°СЂ СѓСЃРїРµС€РЅРѕ СѓРґР°Р»РµРЅ.')
    return redirect(url_for('admin_panel.products'))

# РЈРїСЂР°РІР»РµРЅРёРµ Р±Р»РѕРіРѕРј
@admin_bp.route('/blog/topics')
@admin_required
def blog_topics():
    topics = BlogTopic.query.all()
    return render_template('admin/blog/topics.html', topics=topics)

@admin_bp.route('/blog/categories')
@admin_required
def blog_categories():
    categories = BlogCategory.query.all()
    return render_template('admin/blog/categories.html', categories=categories)

@admin_bp.route('/blog/categories/create', methods=['GET', 'POST'])
@admin_required
def create_blog_category():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        # РњРЅРѕРіРѕСЏР·С‹С‡РЅС‹Рµ РїРѕР»СЏ
        name_uk = request.form.get('name_uk')
        name_de = request.form.get('name_de')
        name_en = request.form.get('name_en')
        description_uk = request.form.get('description_uk')
        description_de = request.form.get('description_de')
        description_en = request.form.get('description_en')
        
        # РЎРѕР·РґР°РµРј slug РёР· РёРјРµРЅРё
        slug = slugify(name)
        
        # РџСЂРѕРІРµСЂСЏРµРј СѓРЅРёРєР°Р»СЊРЅРѕСЃС‚СЊ slug
        if BlogCategory.query.filter_by(slug=slug).first():
            slug = f"{slug}-{uuid.uuid4().hex[:6]}"
        
        # РЎРѕР·РґР°РµРј РЅРѕРІСѓСЋ РєР°С‚РµРіРѕСЂРёСЋ Р±Р»РѕРіР°
        category = BlogCategory(
            name=name,
            slug=slug,
            description=description,
            name_uk=name_uk,
            name_de=name_de,
            name_en=name_en,
            description_uk=description_uk,
            description_de=description_de,
            description_en=description_en
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash('РљР°С‚РµРіРѕСЂРёСЏ Р±Р»РѕРіР° СѓСЃРїРµС€РЅРѕ СЃРѕР·РґР°РЅР°.')
        return redirect(url_for('admin_panel.blog_categories'))
    
    return render_template('admin/blog/create_category.html')

@admin_bp.route('/blog/categories/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_blog_category(id):
    category = BlogCategory.query.get_or_404(id)
    
    if request.method == 'POST':
        category.name = request.form.get('name')
        category.description = request.form.get('description')
        
        # РњРЅРѕРіРѕСЏР·С‹С‡РЅС‹Рµ РїРѕР»СЏ
        category.name_uk = request.form.get('name_uk')
        category.name_de = request.form.get('name_de')
        category.name_en = request.form.get('name_en')
        category.description_uk = request.form.get('description_uk')
        category.description_de = request.form.get('description_de')
        category.description_en = request.form.get('description_en')
        
        db.session.commit()
        flash('РљР°С‚РµРіРѕСЂРёСЏ Р±Р»РѕРіР° СѓСЃРїРµС€РЅРѕ РѕР±РЅРѕРІР»РµРЅР°.')
        return redirect(url_for('admin_panel.blog_categories'))
    
    return render_template('admin/blog/edit_category.html', category=category)

@admin_bp.route('/blog/categories/delete/<int:id>', methods=['POST'])
@admin_required
def delete_blog_category(id):
    category = BlogCategory.query.get_or_404(id)
    
    # РџСЂРѕРІРµСЂСЏРµРј, РµСЃС‚СЊ Р»Рё СЃС‚Р°С‚СЊРё РІ СЌС‚РѕР№ РєР°С‚РµРіРѕСЂРёРё
    if category.posts.count() > 0:
        flash('РќРµРІРѕР·РјРѕР¶РЅРѕ СѓРґР°Р»РёС‚СЊ РєР°С‚РµРіРѕСЂРёСЋ, СЃРѕРґРµСЂР¶Р°С‰СѓСЋ СЃС‚Р°С‚СЊРё.')
        return redirect(url_for('admin_panel.blog_categories'))
    
    db.session.delete(category)
    db.session.commit()
    
    flash('РљР°С‚РµРіРѕСЂРёСЏ Р±Р»РѕРіР° СѓСЃРїРµС€РЅРѕ СѓРґР°Р»РµРЅР°.')
    return redirect(url_for('admin_panel.blog_categories'))

@admin_bp.route('/blog/topics/create', methods=['GET', 'POST'])
@admin_required
def create_blog_topic():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        keywords = request.form.get('keywords')
        language = request.form.get('language')
        is_active = True if request.form.get('is_active') else False
        
        topic = BlogTopic(
            title=title,
            description=description,
            keywords=keywords,
            language=language,
            is_active=is_active
        )
        
        db.session.add(topic)
        db.session.commit()
        
        flash('РўРµРјР° РґР»СЏ Р±Р»РѕРіР° СѓСЃРїРµС€РЅРѕ СЃРѕР·РґР°РЅР°.')
        return redirect(url_for('admin_panel.blog_topics'))
    
    return render_template('admin/blog/create_topic.html')

@admin_bp.route('/blog/topics/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_blog_topic(id):
    topic = BlogTopic.query.get_or_404(id)
    
    if request.method == 'POST':
        topic.title = request.form.get('title')
        topic.description = request.form.get('description')
        topic.keywords = request.form.get('keywords')
        topic.language = request.form.get('language')
        topic.is_active = True if request.form.get('is_active') else False
        
        db.session.commit()
        
        flash('РўРµРјР° РґР»СЏ Р±Р»РѕРіР° СѓСЃРїРµС€РЅРѕ РѕР±РЅРѕРІР»РµРЅР°.')
        return redirect(url_for('admin_panel.blog_topics'))
    
    return render_template('admin/blog/edit_topic.html', topic=topic)

@admin_bp.route('/blog/topics/delete/<int:id>', methods=['POST'])
@admin_required
def delete_blog_topic(id):
    topic = BlogTopic.query.get_or_404(id)
    
    db.session.delete(topic)
    db.session.commit()
    
    flash('РўРµРјР° РґР»СЏ Р±Р»РѕРіР° СѓСЃРїРµС€РЅРѕ СѓРґР°Р»РµРЅР°.')
    return redirect(url_for('admin_panel.blog_topics'))

@admin_bp.route('/blog/generate', methods=['GET', 'POST'])
@admin_required
def generate_blog():
    if request.method == 'POST':
        topic_id = request.form.get('topic_id')
        category_id = request.form.get('category_id')
        
        topic = BlogTopic.query.get_or_404(topic_id)
        category = BlogCategory.query.get_or_404(category_id)
        
        # Р“РµРЅРµСЂРёСЂСѓРµРј РєРѕРЅС‚РµРЅС‚ СЃ РїРѕРјРѕС‰СЊСЋ OpenAI
        content = generate_blog_post(topic.title, topic.language)
        
        if content:
            # РЎРѕР·РґР°РµРј Р·Р°РіРѕР»РѕРІРѕРє РёР· С‚РµРјС‹
            title = topic.title
            
            # РЎРѕР·РґР°РµРј slug РёР· Р·Р°РіРѕР»РѕРІРєР°
            slug = slugify(title)
            
            # РџСЂРѕРІРµСЂСЏРµРј СѓРЅРёРєР°Р»СЊРЅРѕСЃС‚СЊ slug
            if BlogPost.query.filter_by(slug=slug).first():
                slug = f"{slug}-{uuid.uuid4().hex[:6]}"
            
            # РЎРѕР·РґР°РµРј РЅРѕРІСѓСЋ СЃС‚Р°С‚СЊСЋ
            post = BlogPost(
                title=title,
                slug=slug,
                content=content,
                is_published=True,
                is_auto_generated=True,
                category_id=category_id,
                meta_title=title,
                meta_description=topic.description[:300] if topic.description else title,
                meta_keywords=topic.keywords
            )
            
            # Р—Р°РїРѕР»РЅСЏРµРј РїРѕР»СЏ РґР»СЏ СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓСЋС‰РµРіРѕ СЏР·С‹РєР°
            if topic.language == 'uk':
                post.title_uk = title
                post.content_uk = content
                post.meta_title_uk = title
                post.meta_description_uk = topic.description[:300] if topic.description else title
                post.meta_keywords_uk = topic.keywords
            elif topic.language == 'de':
                post.title_de = title
                post.content_de = content
                post.meta_title_de = title
                post.meta_description_de = topic.description[:300] if topic.description else title
                post.meta_keywords_de = topic.keywords
            else:  # en
                post.title_en = title
                post.content_en = content
                post.meta_title_en = title
                post.meta_description_en = topic.description[:300] if topic.description else title
                post.meta_keywords_en = topic.keywords
            
            db.session.add(post)
            db.session.commit()
            
            flash('РЎС‚Р°С‚СЊСЏ СѓСЃРїРµС€РЅРѕ СЃРіРµРЅРµСЂРёСЂРѕРІР°РЅР° Рё РѕРїСѓР±Р»РёРєРѕРІР°РЅР°.')
            return redirect(url_for('admin_panel.blog_topics'))
        else:
            flash('РћС€РёР±РєР° РїСЂРё РіРµРЅРµСЂР°С†РёРё СЃС‚Р°С‚СЊРё. РџРѕР¶Р°Р»СѓР№СЃС‚Р°, РїСЂРѕРІРµСЂСЊС‚Рµ РЅР°СЃС‚СЂРѕР№РєРё OpenAI API.')
    
    topics = BlogTopic.query.filter_by(is_active=True).all()
    categories = BlogCategory.query.all()
    
    return render_template('admin/blog/generate.html', topics=topics, categories=categories)

# РЈРїСЂР°РІР»РµРЅРёРµ РЅР°СЃС‚СЂРѕР№РєР°РјРё СЃР°Р№С‚Р°
@admin_bp.route('/settings')
@admin_required
def settings():
    social_links = SocialLink.query.order_by(SocialLink.order).all()
    site_settings = SiteSettings.query.all()
    
    return render_template('admin/settings/index.html', social_links=social_links, site_settings=site_settings)

@admin_bp.route('/settings/social/create', methods=['GET', 'POST'])
@admin_required
def create_social_link():
    if request.method == 'POST':
        name = request.form.get('name')
        url = request.form.get('url')
        icon = request.form.get('icon')
        order = int(request.form.get('order', 0))
        is_active = True if request.form.get('is_active') else False
        
        social_link = SocialLink(
            name=name,
            url=url,
            icon=icon,
            order=order,
            is_active=is_active
        )
        
        db.session.add(social_link)
        db.session.commit()
        
        flash('РЎСЃС‹Р»РєР° РЅР° СЃРѕС†СЃРµС‚СЊ СѓСЃРїРµС€РЅРѕ РґРѕР±Р°РІР»РµРЅР°.')
        return redirect(url_for('admin_panel.settings'))
    
    return render_template('admin/settings/create_social.html')

@admin_bp.route('/settings/site/edit/<key>', methods=['GET', 'POST'])
@admin_required
def edit_site_setting(key):
    setting = SiteSettings.query.filter_by(key=key).first()
    
    if not setting:
        setting = SiteSettings(key=key)
        db.session.add(setting)
        db.session.commit()
    
    if request.method == 'POST':
        setting.value = request.form.get('value')
        setting.value_uk = request.form.get('value_uk')
        setting.value_de = request.form.get('value_de')
        setting.value_en = request.form.get('value_en')
        
        db.session.commit()
        
        flash('РќР°СЃС‚СЂРѕР№РєР° СѓСЃРїРµС€РЅРѕ РѕР±РЅРѕРІР»РµРЅР°.')
        return redirect(url_for('admin_panel.settings'))
    
    return render_template('admin/settings/edit_setting.html', setting=setting)
@admin_bp.route('/blog/posts')
@admin_required
def blog_posts():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin/blog/posts.html', posts=posts)

@admin_bp.route('/blog/posts/create', methods=['GET', 'POST'])
@admin_required
def create_blog_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category_id = request.form.get('category_id')
        is_published = True if request.form.get('is_published') else False
        
        # SEO поля
        meta_title = request.form.get('meta_title')
        meta_description = request.form.get('meta_description')
        meta_keywords = request.form.get('meta_keywords')
        
        # Многоязычные поля
        title_uk = request.form.get('title_uk')
        title_de = request.form.get('title_de')
        title_en = request.form.get('title_en')
        content_uk = request.form.get('content_uk')
        content_de = request.form.get('content_de')
        content_en = request.form.get('content_en')
        meta_title_uk = request.form.get('meta_title_uk')
        meta_title_de = request.form.get('meta_title_de')
        meta_title_en = request.form.get('meta_title_en')
        meta_description_uk = request.form.get('meta_description_uk')
        meta_description_de = request.form.get('meta_description_de')
        meta_description_en = request.form.get('meta_description_en')
        meta_keywords_uk = request.form.get('meta_keywords_uk')
        meta_keywords_de = request.form.get('meta_keywords_de')
        meta_keywords_en = request.form.get('meta_keywords_en')
        
        # Создаем slug из заголовка
        slug = slugify(title)
        
        # Проверяем уникальность slug
        if BlogPost.query.filter_by(slug=slug).first():
            slug = f"{slug}-{uuid.uuid4().hex[:6]}"
        
        # Обработка загруженного изображения
        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                # Генерируем уникальное имя файла
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'blog', unique_filename)
                
                # Создаем директорию, если она не существует
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                file.save(file_path)
                image = f"uploads/blog/{unique_filename}"
        
        # Создаем новую статью
        post = BlogPost(
            title=title,
            slug=slug,
            content=content,
            image=image,
            is_published=is_published,
            is_auto_generated=False,
            category_id=category_id,
            meta_title=meta_title,
            meta_description=meta_description,
            meta_keywords=meta_keywords,
            title_uk=title_uk,
            title_de=title_de,
            title_en=title_en,
            content_uk=content_uk,
            content_de=content_de,
            content_en=content_en,
            meta_title_uk=meta_title_uk,
            meta_title_de=meta_title_de,
            meta_title_en=meta_title_en,
            meta_description_uk=meta_description_uk,
            meta_description_de=meta_description_de,
            meta_description_en=meta_description_en,
            meta_keywords_uk=meta_keywords_uk,
            meta_keywords_de=meta_keywords_de,
            meta_keywords_en=meta_keywords_en
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash('Статья успешно создана.')
        return redirect(url_for('admin_panel.blog_posts'))
    
    categories = BlogCategory.query.all()
    return render_template('admin/blog/create_post.html', categories=categories)

@admin_bp.route('/blog/posts/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_blog_post(id):
    post = BlogPost.query.get_or_404(id)
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.category_id = request.form.get('category_id')
        post.is_published = True if request.form.get('is_published') else False
        
        # SEO поля
        post.meta_title = request.form.get('meta_title')
        post.meta_description = request.form.get('meta_description')
        post.meta_keywords = request.form.get('meta_keywords')
        
        # Многоязычные поля
        post.title_uk = request.form.get('title_uk')
        post.title_de = request.form.get('title_de')
        post.title_en = request.form.get('title_en')
        post.content_uk = request.form.get('content_uk')
        post.content_de = request.form.get('content_de')
        post.content_en = request.form.get('content_en')
        post.meta_title_uk = request.form.get('meta_title_uk')
        post.meta_title_de = request.form.get('meta_title_de')
        post.meta_title_en = request.form.get('meta_title_en')
        post.meta_description_uk = request.form.get('meta_description_uk')
        post.meta_description_de = request.form.get('meta_description_de')
        post.meta_description_en = request.form.get('meta_description_en')
        post.meta_keywords_uk = request.form.get('meta_keywords_uk')
        post.meta_keywords_de = request.form.get('meta_keywords_de')
        post.meta_keywords_en = request.form.get('meta_keywords_en')
        
        # Обработка загруженного изображения
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                # Генерируем уникальное имя файла
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'blog', unique_filename)
                
                # Создаем директорию, если она не существует
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                file.save(file_path)
                
                # Удаляем старое изображение, если оно существует
                if post.image:
                    old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], post.image.replace('uploads/', ''))
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                post.image = f"uploads/blog/{unique_filename}"
        
        db.session.commit()
        flash('Статья успешно обновлена.')
        return redirect(url_for('admin_panel.blog_posts'))
    
    categories = BlogCategory.query.all()
    return render_template('admin/blog/edit_post.html', post=post, categories=categories)

@admin_bp.route('/blog/posts/delete/<int:id>', methods=['POST'])
@admin_required
def delete_blog_post(id):
    post = BlogPost.query.get_or_404(id)
    
    # Удаляем изображение, если оно существует
    if post.image:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], post.image.replace('uploads/', ''))
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(post)
    db.session.commit()
    
    flash('Статья успешно удалена.')
    return redirect(url_for('admin_panel.blog_posts'))


# Маршруты для управления постами блога

    
    categories = BlogCategory.query.all()
    return render_template("admin/blog/create_post.html", categories=categories)

@admin_bp.route("/blog/posts/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_blog_post(id):
    post = BlogPost.query.get_or_404(id)
    
    if request.method == "POST":
        post.title = request.form.get("title")
        post.content = request.form.get("content")
        post.category_id = request.form.get("category_id")
        post.is_published = True if request.form.get("is_published") else False
        
        # SEO поля
        post.meta_title = request.form.get("meta_title")
        post.meta_description = request.form.get("meta_description")
        post.meta_keywords = request.form.get("meta_keywords")
        
        # Многоязычные поля
        post.title_uk = request.form.get("title_uk")
        post.title_de = request.form.get("title_de")
        post.title_en = request.form.get("title_en")
        post.content_uk = request.form.get("content_uk")
        post.content_de = request.form.get("content_de")
        post.content_en = request.form.get("content_en")
        post.meta_title_uk = request.form.get("meta_title_uk")
        post.meta_title_de = request.form.get("meta_title_de")
        post.meta_title_en = request.form.get("meta_title_en")
        post.meta_description_uk = request.form.get("meta_description_uk")
        post.meta_description_de = request.form.get("meta_description_de")
        post.meta_description_en = request.form.get("meta_description_en")
        post.meta_keywords_uk = request.form.get("meta_keywords_uk")
        post.meta_keywords_de = request.form.get("meta_keywords_de")
        post.meta_keywords_en = request.form.get("meta_keywords_en")
        
        # Обработка загруженного изображения
        if "image" in request.files:
            file = request.files["image"]
            if file and file.filename:
                filename = secure_filename(file.filename)
                # Генерируем уникальное имя файла
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], "blog", unique_filename)
                
                # Создаем директорию, если она не существует
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                file.save(file_path)
                
                # Удаляем старое изображение, если оно существует
                if post.image:
                    old_image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], post.image.replace("uploads/", ""))
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                post.image = f"uploads/blog/{unique_filename}"
        
        db.session.commit()
        flash("Статья успешно обновлена.")
        return redirect(url_for("admin_panel.blog_posts"))
    
    categories = BlogCategory.query.all()
    return render_template("admin/blog/edit_post.html", post=post, categories=categories)

@admin_bp.route("/blog/posts/delete/<int:id>", methods=["POST"])
@admin_required
def delete_blog_post(id):
    post = BlogPost.query.get_or_404(id)
    
    # Удаляем изображение, если оно существует
    if post.image:
        image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], post.image.replace("uploads/", ""))
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(post)
    db.session.commit()
    
    flash("Статья успешно удалена.")
    return redirect(url_for("admin_panel.blog_posts"))




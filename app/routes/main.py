from flask import Blueprint, render_template, redirect, url_for, session, request
from app.models.product import Category, Product
from app.models.blog import BlogPost
from app.models.settings import SocialLink, SiteSettings

main_bp = Blueprint('main', __name__)

from datetime import datetime

@main_bp.route('/')
def index():
    # Получаем категории товаров для отображения на главной странице
    categories = Category.query.limit(4).all()
    
    # Получаем последние статьи блога
    recent_posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.created_at.desc()).limit(3).all()
    
    # Получаем социальные ссылки для хедера
    social_links = SocialLink.query.filter_by(is_active=True).order_by(SocialLink.order).all()
    
    return render_template('main/index.html', 
                          categories=categories, 
                          recent_posts=recent_posts,
                          social_links=social_links,
                          now=datetime.now())

@main_bp.route('/set_language/<language>')
def set_language(language):
    # Проверяем, что язык поддерживается
    if language in ['uk', 'de', 'en']:
        session['language'] = language
    return redirect(request.referrer or url_for('main.index'))

@main_bp.route('/privacy')
def privacy():
    privacy_content = SiteSettings.query.filter_by(key='privacy_policy').first()
    return render_template('main/page.html', title='Политика конфиденциальности', content=privacy_content)

@main_bp.route('/terms')
def terms():
    terms_content = SiteSettings.query.filter_by(key='terms_conditions').first()
    return render_template('main/page.html', title='Условия использования', content=terms_content)

@main_bp.route('/impressum')
def impressum():
    impressum_content = SiteSettings.query.filter_by(key='impressum').first()
    return render_template('main/page.html', title='Импрессум', content=impressum_content)
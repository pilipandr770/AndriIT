from datetime import datetime
from app import db

from app.models.base import TABLE_ARGS

class BlogCategory(db.Model):
    __tablename__ = 'blog_categories'
    __table_args__ = TABLE_ARGS
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Поля для многоязычности
    name_uk = db.Column(db.String(100))
    name_de = db.Column(db.String(100))
    name_en = db.Column(db.String(100))
    description_uk = db.Column(db.Text)
    description_de = db.Column(db.Text)
    description_en = db.Column(db.Text)
    
    # Отношения
    posts = db.relationship('BlogPost', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<BlogCategory {self.name}>'

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    __table_args__ = TABLE_ARGS
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255))
    is_published = db.Column(db.Boolean, default=True)
    is_auto_generated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('AndriIT.blog_categories.id' if TABLE_ARGS else 'blog_categories.id'))
    
    # SEO поля
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.String(300))
    meta_keywords = db.Column(db.String(200))
    
    # Поля для многоязычности
    title_uk = db.Column(db.String(200))
    title_de = db.Column(db.String(200))
    title_en = db.Column(db.String(200))
    content_uk = db.Column(db.Text)
    content_de = db.Column(db.Text)
    content_en = db.Column(db.Text)
    meta_title_uk = db.Column(db.String(200))
    meta_title_de = db.Column(db.String(200))
    meta_title_en = db.Column(db.String(200))
    meta_description_uk = db.Column(db.String(300))
    meta_description_de = db.Column(db.String(300))
    meta_description_en = db.Column(db.String(300))
    meta_keywords_uk = db.Column(db.String(200))
    meta_keywords_de = db.Column(db.String(200))
    meta_keywords_en = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<BlogPost {self.title}>'

class BlogTopic(db.Model):
    __tablename__ = 'blog_topics'
    __table_args__ = TABLE_ARGS
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    keywords = db.Column(db.String(300))
    language = db.Column(db.String(2), default='uk')  # uk, de, en
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BlogTopic {self.title}>'
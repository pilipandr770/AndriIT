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
from app.routes.admin import admin_bp, admin_required

# Маршруты для управления постами блога

@admin_bp.route("/blog/posts")
@admin_required
def blog_posts():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template("admin/blog/posts.html", posts=posts)

@admin_bp.route("/blog/posts/create", methods=["GET", "POST"])
@admin_required
def create_blog_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        category_id = request.form.get("category_id")
        is_published = True if request.form.get("is_published") else False
        
        # SEO поля
        meta_title = request.form.get("meta_title")
        meta_description = request.form.get("meta_description")
        meta_keywords = request.form.get("meta_keywords")
        
        # Многоязычные поля
        title_uk = request.form.get("title_uk")
        title_de = request.form.get("title_de")
        title_en = request.form.get("title_en")
        content_uk = request.form.get("content_uk")
        content_de = request.form.get("content_de")
        content_en = request.form.get("content_en")
        meta_title_uk = request.form.get("meta_title_uk")
        meta_title_de = request.form.get("meta_title_de")
        meta_title_en = request.form.get("meta_title_en")
        meta_description_uk = request.form.get("meta_description_uk")
        meta_description_de = request.form.get("meta_description_de")
        meta_description_en = request.form.get("meta_description_en")
        meta_keywords_uk = request.form.get("meta_keywords_uk")
        meta_keywords_de = request.form.get("meta_keywords_de")
        meta_keywords_en = request.form.get("meta_keywords_en")
        
        # Создаем slug из заголовка
        slug = slugify(title)
        
        # Проверяем уникальность slug
        if BlogPost.query.filter_by(slug=slug).first():
            slug = f"{slug}-{uuid.uuid4().hex[:6]}"
        
        # Обработка загруженного изображения
        image = None
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
        
        flash("Статья успешно создана.")
        return redirect(url_for("admin_panel.blog_posts"))
    
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

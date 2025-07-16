from flask import Blueprint, render_template, redirect, url_for, request, current_app
from app.models.blog import BlogPost, BlogCategory
import openai

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False)
    
    categories = BlogCategory.query.all()
    
    return render_template('blog/index.html', posts=posts, categories=categories)

@blog_bp.route('/category/<slug>')
def category(slug):
    category = BlogCategory.query.filter_by(slug=slug).first_or_404()
    
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    posts = BlogPost.query.filter_by(category_id=category.id, is_published=True).order_by(
        BlogPost.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('blog/category.html', category=category, posts=posts)

@blog_bp.route('/post/<slug>')
def post(slug):
    post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()
    
    # Получаем похожие посты из той же категории
    related_posts = BlogPost.query.filter(
        BlogPost.category_id == post.category_id,
        BlogPost.id != post.id,
        BlogPost.is_published == True
    ).order_by(BlogPost.created_at.desc()).limit(3).all()
    
    return render_template('blog/post.html', post=post, related_posts=related_posts)

def generate_blog_post(topic, language='uk'):
    """
    Генерирует содержимое блога с помощью OpenAI API
    """
    try:
        # Инициализируем клиент OpenAI с API ключом
        from openai import OpenAI
        # Create client with only the required parameters
        api_key = current_app.config['OPENAI_API_KEY']
        client = OpenAI(api_key=api_key)
        
        # Определяем язык для промпта
        if language == 'uk':
            system_prompt = "Ти - експерт з написання SEO-оптимізованих статей для блогу. Напиши статтю українською мовою."
        elif language == 'de':
            system_prompt = "Du bist ein Experte für das Schreiben von SEO-optimierten Blogartikeln. Schreibe einen Artikel auf Deutsch."
        else:  # en
            system_prompt = "You are an expert in writing SEO-optimized blog articles. Write an article in English."
        
        # Создаем промпт для генерации статьи
        user_prompt = f"Напиши SEO-оптимизированную статью на тему: {topic}. Статья должна быть информативной, содержать подзаголовки, списки и быть оптимизированной для поисковых систем."
        
        # Вызываем API OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=2000
        )
        
        # Возвращаем сгенерированный текст
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Ошибка при генерации статьи: {str(e)}")
        return None
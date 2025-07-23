"""
Минимальное приложение Flask без зависимостей от Flask-Admin
"""
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Минимальное приложение Flask</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                line-height: 1.6;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            h1 {
                color: #333;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Приложение успешно запущено!</h1>
            <p>Это минимальное приложение Flask, которое работает без Flask-Admin.</p>
            <p>Основное приложение временно недоступно из-за проблем с зависимостями.</p>
            <p>Мы работаем над решением этой проблемы.</p>
        </div>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True)
#!/usr/bin/env python
"""
Альтернативный запуск приложения с fallback
"""
import os

def main():
    try:
        # Пробуем запустить основное приложение
        from app import create_app
        app = create_app()
        print("✅ Основное приложение загружено успешно")
        return app
    except Exception as e:
        print(f"❌ Ошибка загрузки основного приложения: {e}")
        try:
            # Fallback к простому приложению
            from simple_app import create_simple_app
            app = create_simple_app()
            print("⚠️ Загружено простое fallback приложение")
            return app
        except Exception as fallback_error:
            print(f"❌ Ошибка fallback приложения: {fallback_error}")
            # Создаем самое минимальное приложение
            from flask import Flask, jsonify
            app = Flask(__name__)
            
            @app.route('/')
            def emergency():
                return jsonify({
                    'status': 'emergency',
                    'message': 'Emergency Flask app is running',
                    'error': str(e)
                })
            
            print("🚨 Запущено экстренное приложение")
            return app

# Создаем приложение
app = main()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

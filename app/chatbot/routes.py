from flask import Blueprint, request, jsonify, session
from app.chatbot.openai_client import chatbot
import time

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

@chatbot_bp.route('/start', methods=['POST'])
def start_chat():
    """Начало нового чата"""
    try:
        # Создаем новый поток для диалога
        thread_id = chatbot.create_thread()
        
        # Сохраняем ID потока в сессии пользователя
        session['chatbot_thread_id'] = thread_id
        
        return jsonify({
            'success': True,
            'thread_id': thread_id,
            'message': 'Чат успешно начат'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chatbot_bp.route('/send', methods=['POST'])
def send_message():
    """Отправка сообщения чат-боту"""
    try:
        data = request.json
        message = data.get('message')
        language = data.get('language', 'uk')  # Язык по умолчанию - украинский
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'Сообщение не может быть пустым'
            }), 400
        
        # Получаем ID потока из сессии или создаем новый
        thread_id = session.get('chatbot_thread_id')
        if not thread_id:
            thread_id = chatbot.create_thread()
            session['chatbot_thread_id'] = thread_id
        
        # Добавляем сообщение пользователя в поток
        chatbot.add_message(thread_id, message, language)
        
        # Запускаем ассистента для обработки сообщения
        run_id = chatbot.run_assistant(thread_id)
        
        # Ждем завершения обработки (в реальном приложении лучше использовать асинхронный подход)
        status = chatbot.get_run_status(thread_id, run_id)
        max_attempts = 30
        attempts = 0
        
        while status not in ['completed', 'failed', 'expired'] and attempts < max_attempts:
            time.sleep(1)
            status = chatbot.get_run_status(thread_id, run_id)
            attempts += 1
        
        if status != 'completed':
            return jsonify({
                'success': False,
                'error': f'Ошибка обработки сообщения: {status}'
            }), 500
        
        # Получаем последние сообщения из потока
        messages = chatbot.get_messages(thread_id, limit=2)
        
        # Первое сообщение должно быть от ассистента (ответ на запрос пользователя)
        assistant_message = next((msg for msg in messages if msg['role'] == 'assistant'), None)
        
        if not assistant_message:
            return jsonify({
                'success': False,
                'error': 'Не удалось получить ответ от ассистента'
            }), 500
        
        return jsonify({
            'success': True,
            'message': assistant_message['content']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chatbot_bp.route('/history', methods=['GET'])
def get_chat_history():
    """Получение истории чата"""
    try:
        thread_id = session.get('chatbot_thread_id')
        
        if not thread_id:
            return jsonify({
                'success': False,
                'error': 'Чат не начат'
            }), 400
        
        # Получаем сообщения из потока
        messages = chatbot.get_messages(thread_id)
        
        return jsonify({
            'success': True,
            'messages': messages
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
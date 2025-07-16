from openai import OpenAI
from flask import current_app
import json

class ChatbotClient:
    def __init__(self):
        self.client = None
        self.assistant_id = None
    
    def initialize(self):
        """Инициализация клиента OpenAI"""
        api_key = current_app.config.get('OPENAI_API_KEY')
        self.assistant_id = current_app.config.get('OPENAI_ASSISTANT_ID')
        
        if not api_key:
            raise ValueError("OpenAI API key is not configured")
        
        self.client = OpenAI(api_key=api_key)
    
    def create_thread(self):
        """Создание нового потока диалога"""
        if not self.client:
            self.initialize()
        
        thread = self.client.beta.threads.create()
        return thread.id
    
    def add_message(self, thread_id, message, language='uk'):
        """Добавление сообщения пользователя в поток"""
        if not self.client:
            self.initialize()
        
        # Добавляем информацию о языке пользователя
        message_with_lang = f"[Language: {language}] {message}"
        
        message = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message_with_lang
        )
        return message.id
    
    def run_assistant(self, thread_id):
        """Запуск ассистента для обработки потока"""
        if not self.client:
            self.initialize()
        
        if not self.assistant_id:
            raise ValueError("OpenAI Assistant ID is not configured")
        
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id
        )
        return run.id
    
    def get_run_status(self, thread_id, run_id):
        """Получение статуса выполнения"""
        if not self.client:
            self.initialize()
        
        run = self.client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        return run.status
    
    def get_messages(self, thread_id, limit=10):
        """Получение сообщений из потока"""
        if not self.client:
            self.initialize()
        
        messages = self.client.beta.threads.messages.list(
            thread_id=thread_id,
            limit=limit
        )
        
        formatted_messages = []
        for msg in messages.data:
            content = msg.content[0].text.value if msg.content else ""
            formatted_messages.append({
                'id': msg.id,
                'role': msg.role,
                'content': content,
                'created_at': msg.created_at
            })
        
        return formatted_messages

# Создаем экземпляр клиента
chatbot = ChatbotClient()
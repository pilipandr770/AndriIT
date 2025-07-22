// Функционал чат-бота

document.addEventListener('DOMContentLoaded', function() {
    // Элементы чат-бота
    const chatbotWidget = document.getElementById('chatbotWidget');
    const chatbotHeader = document.getElementById('chatbotHeader');
    const chatbotBody = document.getElementById('chatbotBody');
    const chatbotToggle = document.getElementById('chatbotToggle');
    const chatbotMessages = document.getElementById('chatbotMessages');
    const chatbotInput = document.getElementById('chatbotInput');
    const chatbotSend = document.getElementById('chatbotSend');
    
    // Добавляем новые элементы для улучшенного интерфейса
    const chatbotControls = document.createElement('div');
    chatbotControls.className = 'chatbot-controls';
    chatbotControls.innerHTML = `
        <button id="chatbotClear" class="chatbot-control-btn" title="Очистить историю">
            <i class="fas fa-trash"></i>
        </button>
    `;
    chatbotHeader.appendChild(chatbotControls);
    
    const chatbotClear = document.getElementById('chatbotClear');
    
    // Создаем кнопку быстрого доступа к чат-боту
    const quickAccessButton = document.createElement('div');
    quickAccessButton.className = 'chatbot-quick-access';
    quickAccessButton.innerHTML = '<i class="fas fa-robot"></i>';
    quickAccessButton.style.display = 'none'; // Изначально скрыта
    document.body.appendChild(quickAccessButton);
    
    // Состояние чат-бота
    let isChatbotOpen = false; // По умолчанию чат-бот закрыт
    let threadStarted = false;
    let isProcessing = false; // Флаг для отслеживания обработки сообщения
    
    // Функция для переключения состояния чат-бота
    function toggleChatbot() {
        if (isChatbotOpen) {
            chatbotBody.style.display = 'none';
            chatbotToggle.innerHTML = '<i class="fas fa-chevron-down"></i>';
            quickAccessButton.style.display = 'flex'; // Показываем кнопку быстрого доступа
        } else {
            chatbotBody.style.display = 'flex';
            chatbotToggle.innerHTML = '<i class="fas fa-chevron-up"></i>';
            quickAccessButton.style.display = 'none'; // Скрываем кнопку быстрого доступа
            
            // Если чат еще не начат, инициализируем его
            if (!threadStarted) {
                startChatThread();
            }
            
            // Фокус на поле ввода
            chatbotInput.focus();
        }
        isChatbotOpen = !isChatbotOpen;
    }
    
    // Функция для начала нового чата
    function startChatThread() {
        showLoadingIndicator();
        
        fetch('/api/chatbot/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            hideLoadingIndicator();
            
            if (data.success) {
                threadStarted = true;
                console.log('Чат успешно начат:', data.thread_id);
            } else {
                console.error('Ошибка при начале чата:', data.error);
                addBotMessage('Извините, не удалось инициализировать чат. Пожалуйста, попробуйте позже.');
            }
        })
        .catch(error => {
            hideLoadingIndicator();
            console.error('Ошибка при запросе к API:', error);
            addBotMessage('Извините, произошла ошибка при подключении к серверу.');
        });
    }
    
    // Функция для отправки сообщения
    function sendMessage() {
        const message = chatbotInput.value.trim();
        if (!message || isProcessing) return;
        
        // Добавляем сообщение пользователя в чат
        addUserMessage(message);
        chatbotInput.value = '';
        
        // Показываем индикатор загрузки
        showLoadingIndicator();
        isProcessing = true;
        
        // Если чат еще не начат, инициализируем его
        if (!threadStarted) {
            startChatThread();
        }
        
        // Получаем текущий язык из сессии или используем украинский по умолчанию
        const language = document.documentElement.lang || 'uk';
        
        // Отправляем сообщение на сервер
        fetch('/api/chatbot/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                language: language
            })
        })
        .then(response => response.json())
        .then(data => {
            hideLoadingIndicator();
            isProcessing = false;
            
            if (data.success) {
                addBotMessage(data.message);
            } else {
                console.error('Ошибка при отправке сообщения:', data.error);
                addBotMessage('Извините, произошла ошибка при обработке вашего сообщения.');
            }
        })
        .catch(error => {
            hideLoadingIndicator();
            isProcessing = false;
            
            console.error('Ошибка при запросе к API:', error);
            addBotMessage('Извините, произошла ошибка при подключении к серверу.');
        });
    }
    
    // Функция для добавления сообщения пользователя в чат
    function addUserMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user';
        messageDiv.innerHTML = `<div class="message-content">${text}</div>`;
        chatbotMessages.appendChild(messageDiv);
        scrollToBottom();
    }
    
    // Функция для добавления сообщения бота в чат
    function addBotMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot';
        messageDiv.innerHTML = `<div class="message-content">${text}</div>`;
        chatbotMessages.appendChild(messageDiv);
        scrollToBottom();
    }
    
    // Функция для показа индикатора загрузки
    function showLoadingIndicator() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message bot loading';
        loadingDiv.id = 'chatbotLoading';
        loadingDiv.innerHTML = `
            <div class="message-content">
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        chatbotMessages.appendChild(loadingDiv);
        scrollToBottom();
    }
    
    // Функция для скрытия индикатора загрузки
    function hideLoadingIndicator() {
        const loadingDiv = document.getElementById('chatbotLoading');
        if (loadingDiv) {
            loadingDiv.remove();
        }
    }
    
    // Функция для очистки истории чата
    function clearChatHistory() {
        // Оставляем только приветственное сообщение
        chatbotMessages.innerHTML = `
            <div class="message bot">
                <div class="message-content">Здравствуйте! Я ваш виртуальный помощник. Чем могу помочь?</div>
            </div>
        `;
        
        // Сбрасываем состояние чата
        threadStarted = false;
        
        // Начинаем новый чат при следующем сообщении
        startChatThread();
    }
    
    // Функция для прокрутки чата вниз
    function scrollToBottom() {
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }
    
    // Обработчики событий
    chatbotHeader.addEventListener('click', function(e) {
        // Проверяем, что клик не был на кнопке очистки
        if (!e.target.closest('#chatbotClear')) {
            toggleChatbot();
        }
    });
    
    chatbotSend.addEventListener('click', sendMessage);
    
    chatbotInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    chatbotClear.addEventListener('click', clearChatHistory);
    
    quickAccessButton.addEventListener('click', toggleChatbot);
    
    // Инициализация чат-бота при загрузке страницы
    // По умолчанию чат-бот закрыт
    chatbotBody.style.display = 'none';
    chatbotToggle.innerHTML = '<i class="fas fa-chevron-down"></i>';
    quickAccessButton.style.display = 'flex'; // Показываем кнопку быстрого доступа
});
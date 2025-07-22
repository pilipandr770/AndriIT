# Flask Shop - Интернет-магазин

## 🚨 Проблема совместимости Python 3.13

**Статус:** Render.com в настоящее время использует Python 3.13, который несовместим с SQLAlchemy 2.0+ из-за изменений в системе типов Python.

## 🛠️ Решения для развертывания

### ✅ ВАРИАНТ 1: Минимальное приложение (РЕКОМЕНДУЕТСЯ)

Используется текущая конфигурация в `render.yaml`:
- **Статус:** Работает без проблем
- **Ограничения:** Нет базы данных, только статические страницы
- **URL:** Будет показывать страницу "Flask Shop загружается..."

### 🐳 ВАРИАНТ 2: Docker (Альтернатива)

Если Render поддержит Docker для вашего плана:

1. Измените `render.yaml`:
```yaml
runtime: docker
dockerfilePath: ./Dockerfile
# удалите buildCommand и startCommand
```

2. Или используйте минимальный Docker:
```yaml
dockerfilePath: ./Dockerfile.minimal
```

### 🔧 ВАРИАНТ 3: Другие платформы

Рекомендуемые альтернативы:
- **Heroku** - лучший контроль версий Python
- **Railway** - современная альтернатива
- **DigitalOcean App Platform**
- **PythonAnywhere**

## 📁 Структура файлов

- `run_minimal.py` - Минимальное приложение без БД
- `run_safe.py` - Приложение с fallback механизмами
- `Dockerfile` - Полная версия для Docker
- `Dockerfile.minimal` - Минимальная версия
- `requirements_*.txt` - Различные варианты зависимостей

## 🚀 Быстрый старт на Render

1. Подключите GitHub репозиторий к Render
2. Выберите "Web Service"
3. Render автоматически использует `render.yaml`
4. Добавьте переменные окружения (особенно SECRET_KEY)
5. Нажмите "Deploy"

## 🔑 Переменные окружения

Обязательные:
```
SECRET_KEY=auto-generated
FLASK_DEBUG=0
FLASK_ENV=production
```

Опциональные (для полной версии):
```
DATABASE_URL=your-postgresql-url
OPENAI_API_KEY=your-openai-key
STRIPE_PUBLIC_KEY=your-stripe-key
STRIPE_SECRET_KEY=your-stripe-secret
```

## 📞 Статус и мониторинг

После развертывания проверьте:
- `/` - Главная страница
- `/health` - Проверка состояния
- `/api/status` - API статус

## 🐛 Отладка

Если развертывание не удается:

1. **Проверьте логи** в панели Render
2. **Попробуйте minimal версию:**
   ```yaml
   startCommand: gunicorn --bind 0.0.0.0:$PORT run_minimal:app
   ```
3. **Используйте emergency файл:**
   ```yaml
   pip install Flask==2.0.3 gunicorn==20.1.0
   ```

## 🎯 Планы развития

1. ✅ Минимальная версия работает
2. 🔄 Ожидание исправления совместимости Python 3.13
3. 🚀 Переход на полную версию с БД
4. 📱 Добавление фронтенда

---

**Проект готов к развертыванию на Render!** 🚀

import os
import subprocess
import sys
from pathlib import Path

# Получаем текущую директорию скрипта
script_dir = Path(__file__).parent.absolute()

# Переходим в директорию flask_shop
os.chdir(script_dir)

# Создаем директорию для переводов, если она не существует
os.makedirs('app/translations', exist_ok=True)

# Извлекаем строки для перевода
print("Извлечение строк для перевода...")
subprocess.run(['pybabel', 'extract', '-F', 'babel.cfg', '-o', 'app/translations/messages.pot', '.'])

# Проверяем, существует ли файл messages.pot
if not os.path.exists('app/translations/messages.pot'):
    print("Ошибка: Файл messages.pot не был создан. Проверьте наличие файла babel.cfg и правильность его содержимого.")
    sys.exit(1)

# Обновляем существующие файлы переводов или инициализируем новые
for lang in ['uk', 'de', 'en']:
    lang_file = f'app/translations/{lang}/LC_MESSAGES/messages.po'
    if os.path.exists(lang_file):
        print(f"Обновление файла перевода для языка {lang}...")
        subprocess.run(['pybabel', 'update', '-i', 'app/translations/messages.pot', '-d', 'app/translations', '-l', lang])
    else:
        print(f"Инициализация файла перевода для языка {lang}...")
        subprocess.run(['pybabel', 'init', '-i', 'app/translations/messages.pot', '-d', 'app/translations', '-l', lang])

print("Готово! Теперь вы можете отредактировать файлы переводов в директории app/translations")
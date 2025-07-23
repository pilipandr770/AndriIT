import os
import subprocess

# Компилируем файлы переводов
print("Компиляция файлов переводов...")

# Получаем абсолютный путь к директории flask_shop
flask_shop_dir = os.path.dirname(os.path.abspath(__file__))

for lang in ['uk', 'de', 'en']:
    po_file = os.path.join(flask_shop_dir, f'app/translations/{lang}/LC_MESSAGES/messages.po')
    mo_file = os.path.join(flask_shop_dir, f'app/translations/{lang}/LC_MESSAGES/messages.mo')
    
    if os.path.exists(po_file):
        print(f"Компиляция файла перевода для языка {lang}...")
        subprocess.run(['pybabel', 'compile', '-i', po_file, '-o', mo_file])
    else:
        print(f"Файл перевода для языка {lang} не найден: {po_file}")

print("Готово! Файлы переводов скомпилированы.")
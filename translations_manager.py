import os
import click
from flask import Flask
from flask.cli import with_appcontext
from app import create_app

app = create_app()

@click.group()
def cli():
    """Управление переводами для Flask-Babel."""
    pass

@cli.command()
@with_appcontext
def extract():
    """Извлечение строк для перевода."""
    current_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.system('pybabel extract -F babel.cfg -o app/translations/messages.pot app')
    os.chdir(current_dir)
    click.echo('Строки для перевода извлечены в messages.pot')

@cli.command()
@click.argument('lang')
@with_appcontext
def init(lang):
    """Инициализация нового языка."""
    os.system(f'pybabel init -i app/translations/messages.pot -d app/translations -l {lang}')
    click.echo(f'Язык {lang} инициализирован')

@cli.command()
@with_appcontext
def update():
    """Обновление всех языковых файлов."""
    os.system('pybabel update -i app/translations/messages.pot -d app/translations')
    click.echo('Языковые файлы обновлены')

@cli.command()
@with_appcontext
def compile():
    """Компиляция всех языковых файлов."""
    os.system('pybabel compile -d app/translations')
    click.echo('Языковые файлы скомпилированы')

if __name__ == '__main__':
    cli()
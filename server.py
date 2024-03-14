from waitress import serve
from app.app import main_app
from flask import render_template
import logging
from data import db_session

logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)


@main_app.route('/', defaults={'path': ''})
# @main_app.route('/a/<path:path>')
# @main_app.route('/u/<path:path>')
def root(path):
    return render_template('index.html', title='EventLinker')


@main_app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='Авторизация')


@main_app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', title='Регистрация')

'''Строчка. чтобы создать базу данных'''
db_session.global_init("db/event_linker.db")

if __name__ == '__main__':
    # main_app.run(port=8000, host='127.0.0.1', debug=True)
    serve(main_app, host="127.0.0.1", port=8000)

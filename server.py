from waitress import serve
from app.app import main_app
from flask import render_template
from form.login_form import LoginForm
from form.register_form import RegisterForm
import logging

logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)


@main_app.route('/', defaults={'path': ''})
# @main_app.route('/a/<path:path>')
# @main_app.route('/u/<path:path>')
def root(path):
    '''Главная страница'''
    return render_template('index.html', title='EventLinker')


@main_app.route('/login', methods=['GET', 'POST'])
def login():
    """Страница авторизация"""
    form = LoginForm()
    if form.validate_on_submit():
        pass
    return render_template('login.html', title='Авторизация', form=form)


@main_app.route('/register', methods=['GET', 'POST'])
def register():
    """Страница регистрации"""
    form = RegisterForm()
    if form.validate_on_submit():
        pass
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    # main_app.run(port=8000, host='127.0.0.1', debug=True)
    serve(main_app, host="127.0.0.1", port=8000)

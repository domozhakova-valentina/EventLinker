from waitress import serve
from app.app import main_app
from flask import render_template, redirect
from form.login_form import LoginForm
from form.register_form import RegisterForm
from form.createEvent_form import CreateForm
import logging
from data import db_session

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
        return redirect('/')
    return render_template('login.html', title='Авторизация', form=form)


@main_app.route('/register', methods=['GET', 'POST'])
def register():
    """Страница регистрации"""
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@main_app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    '''Страница - форма создания мероприятия'''
    form = CreateForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('create_event.html', title='Создание мероприятия', form=form)


@main_app.route('/home_user', methods=['GET', 'POST'])
def home_user():
    '''Страница пользователя'''
    return render_template('user_home.html', title='Ваш профиль')


@main_app.route('/user', methods=['GET', 'POST'])
def user():
    '''Профиль на показ всем пользователям'''
    return render_template('user.html', title='Профиль пользователя')


@main_app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    """Редактирование аккаунта пользователя"""
    form = RegisterForm()
    form.submit.label.text = 'Изменить'
    # данные сurrent_user предварительно тут записать в form
    if form.validate_on_submit():
        return redirect('/')
    return render_template('edit_profile.html', title='Редактирование профиля', form=form)


@main_app.route('/delete_user/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
    '''Удаление пользователя'''
    return redirect('/')


'''Строчка. чтобы создать базу данных'''
db_session.global_init("db/event_linker.db")

if __name__ == '__main__':
    # main_app.run(port=8000, host='127.0.0.1', debug=True)
    serve(main_app, host="127.0.0.1", port=8000)

from waitress import serve
from app.app import main_app
from flask import render_template, redirect

from form.addComment_form import AddComment
from form.login_form import LoginForm
from form.register_form import RegisterForm
from form.createEvent_form import CreateForm
import logging
from data import db_session
from form.search_form import SearchForm

logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)


@main_app.route('/', methods=['GET', 'POST'])
def root():
    '''Главная страница'''
    form = SearchForm()  # форма поиска
    if form.validate_on_submit():
        text_search = form.search.data
        # ищем вхождения строки в мини описание или название автора
        data = {'events': []}
    else:
        data = {
            'events': [
                {'id': 1, "image":'static/img/test_icon_user.png', "mini_description":'Мини описание', "username":'Название автора', "create_data":"время создания"},
                {'id': 2, "image":'static/img/test_icon_user.png', "mini_description":'Мини описание', "username":'Название автора', "create_data":"время создания"},
                {'id': 3, "image":'static/img/test_icon_user.png', "mini_description":'Мини описание', "username":'Название автора', "create_data":"время создания"},
                {'id': 4, "image": 'static/img/test_icon_user.png', "mini_description": 'Мини описание',
                 "username": 'Название автора', "create_data": "время создания"}
            ]
        }  # пример использование, когда передаётся в html
    return render_template('index.html', title='EventLinker', data=data, form=form)


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


@main_app.route('/user/<int:id>', methods=['GET', 'POST'])
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


@main_app.route('/event/<int:id>', methods=['GET', 'POST'])
def event(id):
    '''Просмотр события (мероприятия)'''
    form = AddComment()
    if form.validate_on_submit():
        # добавление комментария и перезагрузка
        return redirect(f'/event/{id}')
    return render_template('event.html', form=form, test='<a href="https://lyceum.yandex.ru/">Тест ссылка</a>')


if __name__ == '__main__':
    '''Строчка. чтобы создать базу данных'''
    db_session.global_init("db/event_linker.db")
    # main_app.run(port=8000, host='127.0.0.1', debug=True)
    serve(main_app, host="127.0.0.1", port=8000)

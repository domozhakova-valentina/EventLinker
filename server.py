import flask
from waitress import serve
from app.app import main_app
from flask import render_template, redirect, request
from form.addComment_form import AddComment
from flask import render_template, redirect
from flask_login import LoginManager, login_user, current_user
from form.login_form import LoginForm
from form.register_form import RegisterForm
from form.createEvent_form import CreateForm
from data.users import User
from data.events import Event
from data.comments import Comment
import logging
from form.search_form import SearchForm
from data import db_session

logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)

login_manager = LoginManager()
login_manager.init_app(main_app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


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
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
        return redirect('/')
    return render_template('login.html', title='Авторизация', form=form)


@main_app.route('/register', methods=['GET', 'POST'])
def register():
    """Страница регистрации"""
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form, message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        file = request.files.get('imagefile', '')
        if file:
            user.photo = file.read()
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@main_app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    '''Страница - форма создания мероприятия'''
    form = CreateForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        event = Event()
        file = flask.request.files.get('imagefile', '')
        if file:
            event.photo = file.read()
        event.mini_description = form.mini_description.data
        event.description = form.description.data
        current_user.events.append(event)
        db_sess.merge(current_user)
        db_sess.commit()
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
    if request.method == "GET":
        if current_user:
            form.name.data = current_user.name
            form.email.data = current_user.email
            form.about.data = current_user.about
            # сделать, чтобы отображалась аватарка
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if user:
            user.name = form.name.data
            user.email = form.email.data
            user.about = form.about.data
            file = request.files.get('imagefile', '')
            if file:
                user.photo = file.read()
            # подумать как быть с паролем
            db_sess.commit()
        return redirect('/')
    return render_template('edit_profile.html', title='Редактирование профиля', form=form)


@main_app.route('/delete_user/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    if user:
        db_sess.delete(user)
        db_sess.commit()
    return redirect('/')


@main_app.route('/event/<int:id>', methods=['GET', 'POST'])
def event(id):
    '''Просмотр события (мероприятия)'''
    form = AddComment()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        event = db_sess.query(Event).filter(Event.id == id).first()
        comment = Comment()
        comment.text = form.text_comment.data
        current_user.comments.append(comment)
        event.comments.append(comment)
        db_sess.merge(current_user)
        db_sess.merge(event)
        db_sess.commit()
        return redirect(f'/event/{id}')
    return render_template('event.html', form=form, test='<a href="https://lyceum.yandex.ru/">Тест ссылка</a>')


if __name__ == '__main__':
    '''Строчка. чтобы создать базу данных'''
    db_session.global_init("db/event_linker.db")
    # main_app.run(port=8000, host='127.0.0.1', debug=True)
    serve(main_app, host="127.0.0.1", port=8000)

import flask
from waitress import serve
from app.app import main_app
from flask import render_template, redirect
from flask_login import LoginManager, login_user, current_user
from form.login_form import LoginForm
from form.register_form import RegisterForm
from form.createEvent_form import CreateForm
from data.users import User
from data.events import Event
import logging
from data import db_session

logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)

login_manager = LoginManager()
login_manager.init_app(main_app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


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
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@main_app.route('/register', methods=['GET', 'POST'])
def register():
    """Страница регистрации"""
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data,
            photo=flask.request.files.get('file', '')
        )
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
        event.photo = flask.request.files.get('imagefile', '')
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
    return render_template('user_home.html', title='Страница пользователя')


'''Строчка, чтобы создать базу данных'''
db_session.global_init("db/event_linker.db")

if __name__ == '__main__':
    # main_app.run(port=8000, host='127.0.0.1', debug=True)
    serve(main_app, host="127.0.0.1", port=8000)

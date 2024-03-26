from waitress import serve
from app.app import main_app
from flask import request, jsonify
from form.addComment_form import AddComment
from flask import render_template, redirect
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from form.login_form import LoginForm
from form.register_form import RegisterForm
from form.createEvent_form import CreateForm
from data.users import User
from data.events import Event
from data.comments import Comment
import logging
from form.search_form import SearchForm
from data import db_session
from requests import get, delete

logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)

login_manager = LoginManager()
login_manager.init_app(main_app)
host, port = "127.0.0.1", 8000


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@main_app.route('/logout')
@login_required
def logout():
    '''Обработчик выхода пользователя'''
    logout_user()
    return redirect("/")


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
        if form.about.data.strip() == '':
            form.about.data = form.about.description
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        file = form.photo.data
        if file:
            user.photo = file.read()
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@main_app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    '''Страница - форма создания мероприятия'''
    form = CreateForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        event = Event()
        file = form.photo.data
        if file:
            event.photo = file.read()
        event.mini_description = form.mini_description.data
        event.description = form.description.data
        db_sess.merge(current_user)
        current_user.events.append(event)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('create_event.html', title='Создание мероприятия', form=form)


@main_app.route('/events/<int:id_user>')
def events(id_user):
    '''Просмотр событий (мероприятий), созданных пользователем.'''
    # из БД получаем события
    data = {
        'events': [
            {'id': 1, "image": 'static/img/test_icon_user.png', "mini_description": 'Мини описание',
             "username": 'Название автора', "create_data": "время создания"},
            {'id': 2, "image": 'static/img/test_icon_user.png', "mini_description": 'Мини описание',
             "username": 'Название автора', "create_data": "время создания"},
            {'id': 3, "image": 'static/img/test_icon_user.png', "mini_description": 'Мини описание',
             "username": 'Название автора', "create_data": "время создания"},
            {'id': 4, "image": 'static/img/test_icon_user.png', "mini_description": 'Мини описание',
             "username": 'Название автора', "create_data": "время создания"}
        ]
    }  # пример использование, когда передаётся в html
    user = get(f'http://{host}:{port}/api/v2/users/{id_user}').json()  # объект User из БД
    return render_template('events_user.html', title='Events', data=data, user=user)


@main_app.route('/home_user')
@login_required
def home_user():
    '''Страница пользователя'''
    metrics = {"events": 2, "like_up": 10, "liked": 39, "comments": 4}  # данные-метрики из БД по пользователю
    return render_template('user_home.html', title='Ваш профиль', metrics_user=metrics)


@main_app.route('/user/<int:user_id>', methods=['GET', 'POST'])
def user(user_id):
    '''Профиль на показ всем пользователям'''
    user = get(f'http://{host}:{port}/api/v2/users/{user_id}').json()["user"]  # данные по пользователю
    metrics = {"events": 2, "like_up": 10, "liked": 39, "comments": 4}  # данные-метрики из БД по пользователю
    return render_template('user.html', title='Профиль пользователя', user=user, metrics_user=metrics)


@main_app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Редактирование аккаунта пользователя"""
    form = RegisterForm()
    form.submit.label.text = 'Изменить'
    if request.method == "GET":
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.about.data = current_user.about
        form.photo.data = current_user.photo
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if user:
            if form.about.data.strip() == '':
                form.about.data = form.about.description
            user.name = form.name.data
            user.email = form.email.data
            user.about = form.about.data
            file = form.photo.data
            if file:
                user.photo = file.read()
            # подумать как быть с паролем
            db_sess.commit()
        return redirect('/')
    return render_template('edit_profile.html', title='Редактирование профиля', form=form)


@main_app.route('/delete_user/<int:id>', methods=['GET', 'POST'])
@login_required
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
        db_sess.merge(comment)
        current_user.comments.append(comment)
        event.comments.append(comment)
        db_sess.merge(current_user)
        db_sess.merge(event)
        db_sess.commit()
        return redirect(f'/event/{id}')
    creator_user = object  # создатель события из БД
    response = get(f'http://{host}:{port}/api/v2/events/{id}')
    if response.status_code == 200:
        event = response.json()["event"]  # временно так, информация по событию
        # likes = 10
        comments = {"comments": [{'id': 1, "text": "Комментарий 1......................................",
                    "create_date": 'Дата создания', "create_user": 1, "name_create_user": "Имя пользователя"},
                    {'id': 2, "text": "Комментарий 2......................................",
                     "create_date": 'Дата создания', "create_user": 1, "name_create_user": "Имя пользователя"}
                    ]}  # пример передачи данных
        # комментариев, но можно будет как из базы данных, тогда чуть-чуть переделаю html (напишите мне)
        likes = 1  # тут надо получить количество лайков из БД
        flag_like = True  # поставлен ли на этот пост лайк у пользователя (из БД)
        return render_template('event.html', title="Просмотр события (мероприятия)", form=form,
                               likes=likes, event_id=id, inf_event=event,
                               creator=creator_user, comments=comments["comments"], flag_like=flag_like)
    else:
        return redirect("/")


@main_app.route('/delete_event/<int:event_id>')
@login_required
def delete_event(event_id):
    """Удаление события (мероприятия)"""
    if delete(f'http://{host}:{port}/api/v2/events/{event_id}').status_code == 200:
        return redirect('/')
    return redirect(f"/event/{event_id}")


@main_app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    """Страница редактирования события (мероприятия)"""
    form = CreateForm()
    form.submit.label.text = 'Изменить'
    # дописать логику сохранения прошлых полей
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        event = Event()
        file = form.photo.data
        if file:
            event.photo = file.read()
        event.mini_description = form.mini_description.data
        event.description = form.description.data
        current_user.events.append(event)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('create_event.html', title='Редактирование мероприятия', form=form)


@main_app.route('/delete_comment/<int:event_id>/<int:comment_id>')
@login_required
def delete_comment(event_id, comment_id):
    """Удаление комментария. Может только автор комментария и автор поста!"""
    if delete(f'http://{host}:{port}/api/v2/comments/{comment_id}').status_code == 200:
        pass  # если успеем flash реализовать, то она тут будет
    return redirect(f"/event/{event_id}")


if __name__ == '__main__':
    '''Строчка. чтобы создать базу данных'''
    db_session.global_init("db/event_linker.db")
    serve(main_app, host=host, port=port)

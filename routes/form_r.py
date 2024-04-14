from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_user, login_required, current_user

from data import db_session
from data.events import Event
from data.users import User
from form.createEvent_form import CreateForm
from form.login_form import LoginForm
from form.register_form import RegisterForm

form = Blueprint('form', __name__)


@form.route('/login', methods=['GET', 'POST'])
def login():
    """Страница авторизация"""
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы успешно вошли в учетную запись')
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@form.route('/register', methods=['GET', 'POST'])
def register():
    """Страница регистрации"""
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        if form.about.data.strip() == '':
            form.about.data = form.about.description
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        file = form.photo.data
        if not file:
            file = open("static/img/profil_photo.jpg", "rb")
        user.photo = file.read()
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        flash("Новый пользователь зарегистрирован")
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@form.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    '''Страница - форма создания мероприятия'''
    form = CreateForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        event = Event()
        file = form.photo.data
        if not file:
            file = open("static/img/event_photo.jpg", "rb")
        event.photo = file.read()
        event.mini_description = form.mini_description.data
        event.description = form.description.data
        if not db_sess.is_modified(current_user):
            user = db_sess.merge(current_user)
        # Теперь вы можете безопасно обращаться к атрибуту событий
        user.events.append(event)
        # И снова объедините текущего пользователя в сеансе
        db_sess.merge(user)
        # Произведите фиксацию изменений
        db_sess.commit()
        db_sess.close()
        flash("Новое событие успешно создано")
        return redirect('/')
    return render_template('create_event.html', title='Создание мероприятия', form=form)


@form.route('/edit_profile', methods=['GET', 'POST'])
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
            user.set_password(form.password.data)
            db_sess.commit()
        flash("Данные пользователя успешно изменены")
        return redirect('/')
    return render_template('edit_profile.html', title='Редактирование профиля', form=form)


@form.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    """Страница редактирования события (мероприятия)"""
    session = db_session.create_session()
    if not current_user.id == session.query(Event.create_user).filter(event_id == Event.id).first()[0]:  # переводит пользователя назад, если он не создатель поста
        flash("Вы не имеете право на редактирование этого события!")
        return redirect(f"/event/{event_id}")
    form = CreateForm()
    form.submit.label.text = 'Изменить'
    if request.method == "GET":
        # сохранение прошлых полей
        db_sess = db_session.create_session()
        event = db_sess.query(Event).get(event_id)
        form.mini_description.data = event.mini_description
        form.description.data = event.description
        form.photo.data = event.photo
        db_sess.commit()
        db_sess.close()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        event = db_sess.query(Event).get(event_id)
        file = form.photo.data
        try:
            if file:
                event.photo = file.read()
        except AttributeError:
            event.photo = file
        event.mini_description = form.mini_description.data
        event.description = form.description.data
        db_sess.commit()
        flash("Данные события успешно изменены")
        return redirect('/')
    return render_template('create_event.html', title='Редактирование мероприятия', form=form, event_id=event_id)

from flask import Blueprint, redirect, render_template, flash
from flask_login import login_required, logout_user, current_user

from data import db_session
from data.comments import Comment
from data.events import Event
from data.likes import Like
from data.users import User

rusers = Blueprint('rusers', __name__)


@rusers.route('/logout')
@login_required
def logout():
    '''Обработчик выхода пользователя'''
    logout_user()
    flash('Вы вышли из текущей учётной записи')
    return redirect("/")


@rusers.route('/home_user')
@login_required
def home_user():
    '''Страница пользователя'''
    db_sess = db_session.create_session()
    num_events = db_sess.query(Event).filter(Event.create_user == current_user.id).count()
    num_like_up = db_sess.query(Like).filter(Like.user_id == current_user.id).count()
    events = db_sess.query(Event).filter(Event.create_user == current_user.id).all()
    num_liked = 0
    for event in events:
        num_liked += db_sess.query(Like).filter(Like.event_id == event.id).count()
    num_comments = db_sess.query(Comment).filter(Comment.create_user == current_user.id).count()
    metrics = {"events": num_events, "like_up": num_like_up, "liked": num_liked,
               "comments": num_comments}  # данные-метрики из БД по пользователю
    return render_template('user_home.html', title='Ваш профиль', metrics_user=metrics)


@rusers.route('/user/<int:id>/photo')
def user_photo(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    return rusers.response_class(user.photo, mimetype='application/octet-stream')


@rusers.route('/user/<int:user_id>', methods=['GET', 'POST'])
def user(user_id):
    '''Профиль на показ всем пользователям'''
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)  # данные по пользователю
    num_events = db_sess.query(Event).filter(Event.create_user == user_id).count()
    num_like_up = db_sess.query(Like).filter(Like.user_id == user_id).count()
    events = db_sess.query(Event).filter(Event.create_user == user_id).all()
    num_liked = 0
    for event in events:
        num_liked += db_sess.query(Like).filter(Like.event_id == event.id).count()
    num_comments = db_sess.query(Comment).filter(Comment.create_user == user_id).count()
    metrics = {"events": num_events, "like_up": num_like_up, "liked": num_liked,
               "comments": num_comments}  # данные-метрики из БД по пользователю
    return render_template('user.html', title='Профиль пользователя', user=user, metrics_user=metrics)


@rusers.route('/delete_user/<int:user_id>', methods=['GET'])
@login_required
def delete_user(user_id):
    if current_user.id == user_id:  # проверка, что удаляет пользователь самого себя
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        for id_event in db_sess.query(Like.event_id).filter(user_id == Like.user_id).all():
            # удаление вмести с пользователем всех лайков
            event = db_sess.query(Event).get(id_event)
            if event:
                event.num_likes -= 1
        db_sess.delete(user)
        db_sess.commit()
        flash('Пользователь удален')
        return redirect('/')
    flash('У вас нет права удалять этого пользователя!')
    return redirect('/')


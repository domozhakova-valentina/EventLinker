from flask import Blueprint, redirect, render_template
from flask_login import login_required, current_user
from requests import get, delete, post

from app.app import main_app, host, port
from data import db_session
from data.comments import Comment
from data.events import Event
from data.likes import Like
from data.users import User
from form.addComment_form import AddComment
from form.search_form import SearchForm

revent = Blueprint('revent', __name__)


@revent.route('/', methods=['POST', "GET"])
def root():
    '''Главная страница'''
    form = SearchForm()  # форма поиска
    events = get(f'http://{host}:{port}/api/v2/events').json()['events']  # все существующие события
    data = {'events': []}
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        text_search = form.search.data
        users = get(f'http://{host}:{port}/api/v2/users').json()['users']  # все существующие пользователи

        # ищем вхождения строки в мини-описание или имя автора
        users_id = []
        for user in users:
            if text_search in user['name']:
                users_id.append(user['id'])
        for event in events:
            if text_search in event['mini_description'] or event['create_user'] in users_id:
                data['events'].append(
                    {'id': event['id'],
                     "mini_description": event['mini_description'],
                     "username": db_sess.query(User.name).filter(User.id == event['create_user']).first()[0],
                     "create_date": event['create_date']})

    else:  # отображение всех существующих событий, если форма поиска пустая
        for event in events:
            data['events'].append(
                {'id': event['id'],
                 "mini_description": event['mini_description'],
                 "username": db_sess.query(User.name).filter(User.id == event['create_user']).first()[0],
                 "create_date": event['create_date']})
    db_sess.close()
    return render_template('index.html', title='EventLinker', data=data, form=form)


@revent.route('/events/<int:id_user>')
def events(id_user):
    '''Просмотр событий (мероприятий), созданных пользователем.'''
    # из БД получаем события
    db_sess = db_session.create_session()
    data = db_sess.query(Event).filter(Event.create_user == id_user).all()
    user = get(f'http://{host}:{port}/api/v2/users/{id_user}').json()  # объект User из БД
    return render_template('events_user.html', title='Events', data=data, user=user)


@revent.route('/event/<int:id>/photo')
def event_photo(id):
    db_sess = db_session.create_session()
    event = db_sess.query(Event).filter(Event.id == id).first()
    return main_app.response_class(event.photo, mimetype='application/octet-stream')


@revent.route('/event/<int:id>', methods=['POST', "GET"])
def event(id):
    '''Просмотр события (мероприятия)'''
    form = AddComment()
    if form.validate_on_submit():
        post(f'http://{host}:{port}/api/v2/comments',
             json={'text': form.text_comment.data,
                   'create_user': current_user.id,
                   'event_id': id}).json()
        return redirect(f'/event/{id}')
    db_sess = db_session.create_session()
    creator_user = db_sess.query(User).join(Event,
                                            User.id == Event.create_user).filter(
        Event.id == id).first()  # создатель события из БД
    db_sess = db_session.create_session()
    comments = db_sess.query(Comment).filter(Comment.event_id == id).all()  # список данных каждого комментария
    likes = db_sess.query(Event.num_likes).filter(Event.id == id).first()[
        0]  # количество лайков из БД
    event = db_sess.query(Event).get(id)
    if current_user.is_authenticated:
        like = db_sess.query(Like).filter(Like.event == event, Like.user == current_user).first()
    else:
        like = False
    db_sess.commit()
    flag_like = "true" if like else "false"  # поставлен ли на этот пост лайк у пользователя
    return render_template('event.html', title="Просмотр события (мероприятия)", form=form,
                           likes=likes, event_id=id, inf_event=event,
                           creator=creator_user, comments=comments, flag_like=flag_like)


@revent.route('/delete_event/<int:event_id>')
@login_required
def delete_event(event_id):
    """Удаление события (мероприятия)"""
    if delete(f'http://{host}:{port}/api/v2/events/{event_id}').status_code == 200:
        return redirect('/')
    return redirect(f"/event/{event_id}")


@revent.route('/delete_comment/<int:event_id>/<int:comment_id>')
@login_required
def delete_comment(event_id, comment_id):
    """Удаление комментария. Может только автор комментария и автор поста!"""
    if delete(f'http://{host}:{port}/api/v2/comments/{comment_id}').status_code == 200:
        pass  # если успеем flash реализовать, то она тут будет
    return redirect(f"/event/{event_id}")
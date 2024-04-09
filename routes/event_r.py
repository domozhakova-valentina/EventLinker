from flask import Blueprint, redirect, render_template, flash
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
from data.paginate import Pagination


revent = Blueprint('revent', __name__)


@revent.route('/', methods=['POST', "GET"])
@revent.route('/page/<int:page>', methods=['GET', 'POST'])
def root(page=1):
    '''Главная страница'''
    form = SearchForm()  # форма поиска
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        text_search = form.search.data
        a_events = db_sess.query(Event).join(Event.user).filter(
            (Event.mini_description.like(f'%{text_search}%')) | (User.name.like(f'%{text_search}%')))  # поиск по вхождению в мини-описание или имя автора
    else:
        a_events = db_sess.query(Event).order_by(Event.num_likes.desc())  # сортировка (у которых лайков больше те первые)

    pagination = Pagination(a_events, page, 9)

    return render_template('index.html', title='EventLinker', data=pagination, form=form)


@revent.route('/events/<int:id_user>/page/<int:page>')
def events(id_user, page=1):
    '''Просмотр событий (мероприятий), созданных пользователем.'''
    # из БД получаем события
    db_sess = db_session.create_session()
    data = db_sess.query(Event).filter(Event.create_user == id_user)
    user = get(f'http://{host}:{port}/api/v2/users/{id_user}').json()  # объект User из БД
    pagination = Pagination(data, page, 9)
    return render_template('events_user.html', title='Events', data=pagination, user=user)


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
        flash('Событие удалено')
        return redirect('/')
    return redirect(f"/event/{event_id}")


@revent.route('/delete_comment/<int:event_id>/<int:comment_id>')
@login_required
def delete_comment(event_id, comment_id):
    """Удаление комментария. Может только автор комментария и автор поста!"""
    if delete(f'http://{host}:{port}/api/v2/comments/{comment_id}').status_code == 200:
        flash('Комментарий удален')
    return redirect(f"/event/{event_id}")

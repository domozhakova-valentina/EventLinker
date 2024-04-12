from datetime import datetime

from flask import Blueprint, redirect, render_template, flash
from flask_login import login_required, current_user

from app.app import main_app
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
    user = db_sess.query(User).get(id_user)  # объект User из БД
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
        session = db_session.create_session()
        comment = Comment()
        comment.text = form.text_comment.data
        comment.create_date = datetime.now()
        comment.create_user = current_user.id
        comment.event_id = id
        session.add(comment)
        session.commit()
        session.close()
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
    session = db_session.create_session()
    if current_user.id == session.query(Event.create_user).filter(event_id == Event.id).first()[0]:  # проверка, что удаляет пост создатель его
        try:
            event = session.query(Event).get(event_id)
            session.delete(event)
            session.commit()
            flash('Событие удалено')
        except Exception as ex:
            flash("Не удалось удалить запись!")
        session.close()
        return redirect('/')
    session.close()
    flash('У вас нет прав на удаление этого события')
    return redirect('/')


@revent.route('/delete_comment/<int:user_id>/<int:comment_id>/event=<int:event_id>')
@login_required
def delete_comment(user_id, comment_id, event_id):
    """Удаление комментария. Может только автор комментария или автор поста!"""
    session = db_session.create_session()
    if user_id == current_user.id or current_user.id == \
            session.query(Event.create_user).filter(event_id == Event.id).first()[0]:
        # выше строчка проверки на права удаления комментария (создатель комментария или события)
        try:
            comment = session.query(Comment).get(comment_id)
            session.delete(comment)
            session.commit()
            flash('Комментарий удален')
        except Exception as ex:
            flash("Не удалось удалить запись!")
        session.close()
        return redirect(f"/event/{event_id}")
    session.close()
    flash("Вы не имеете право на удаление этого комментария!")
    return redirect(f"/event/{event_id}")

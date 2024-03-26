from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from data.events import Event
from data.likes import Like
from data.users import User
from flask_login import current_user


def abort_if_event_not_found(event_id):
    session = db_session.create_session()
    event = session.query(Event).get(event_id)
    if not event:
        abort(404, message=f"Event {event_id} not found")


class LikeResource(Resource):
    def post(self, event_id):  # постановка лайка
        abort_if_event_not_found(event_id)
        session = db_session.create_session()
        event = session.query(Event).get(event_id)
        user = session.query(User).get(current_user.id)
        like = Like(event=event, user=user)  # создаем новый объект Like
        session.add(like)
        event.num_likes += 1
        session.commit()
        return jsonify({'likes': event.num_likes, 'message': 'Event liked successfully'})

    def delete(self, event_id):  # удаление лайка
        abort_if_event_not_found(event_id)
        session = db_session.create_session()
        event = session.query(Event).get(event_id)
        like = session.query(Like).filter(Like.event == event, Like.user == current_user).first()
        session.delete(like)
        event.num_likes -= 1
        session.commit()
        return jsonify({'likes': event.num_likes, 'message': 'Like removed successfully'})

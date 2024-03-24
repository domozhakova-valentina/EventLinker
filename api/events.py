from datetime import datetime

from flask import jsonify
from flask_restful import reqparse, abort, Resource

from data import db_session
from data.events import Event
from data.likes import Like
from api.users import abort_if_user_not_found
from data.users import User


def abort_if_event_not_found(event_id):
    session = db_session.create_session()
    event = session.query(Event).get(event_id)
    if not event:
        abort(404, message=f"Event {event_id} not found")


class EventResource(Resource):
    def get(self, event_id):  # информации о конкретном событии
        abort_if_event_not_found(event_id)
        session = db_session.create_session()
        event = session.query(Event).get(event_id)
        return jsonify({'event': event.to_dict(
            only=('id', 'mini_description', 'description', 'create_date', 'num_likes', 'create_user'))})

    # непонятно, что конкретно менять, не делала пока
    def post(self, event_id):
        abort_if_event_not_found(event_id)
        session = db_session.create_session()
        event = session.query(Event).get(event_id)
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, event_id):  # удаление события
        abort_if_event_not_found(event_id)
        session = db_session.create_session()
        event = session.query(Event).get(event_id)
        session.delete(event)
        session.commit()
        return jsonify({'success': 'OK'})

    def event_like(self, event_id, user_id):
        abort_if_event_not_found(event_id)
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        event = session.query(Event).get(event_id)
        user = session.query(User).get(user_id)
        # Проверяем, лайкнул ли уже пользователь событие
        existing_like = Like.query.filter_by(event_id=event.id, user_id=user.id).first()
        if existing_like:
            # Если лайк уже существует, удаляем его
            session.delete(existing_like)
            event.num_likes -= 1
            session.commit()
            return jsonify({'message': 'Like removed successfully'})
        else:
            # Если лайка не существует, создаем новый
            like = Like(event_id=event.id, user_id=user.id)
            session.add(like)
            event.num_likes += 1
            session.commit()
            return jsonify({'message': 'Event liked successfully'})


class EventsListResource(Resource):
    def get(self):  # получение списка событий
        db_sess = db_session.create_session()
        events = db_sess.query(Event).all()
        return jsonify(
            {
                'events':
                    [item.to_dict(
                        only=('id', 'mini_description', 'description', 'create_date', 'num_likes', 'create_user'))
                        for item in events]
            }
        )

    def post(self):  # создание нового события
        parser = reqparse.RequestParser()
        parser.add_argument('mini_description', required=True)
        parser.add_argument('description', required=True)
        parser.add_argument('create_user', required=True, type=int)
        parser.add_argument('num_likes', required=True, type=int)
        args = parser.parse_args()
        session = db_session.create_session()
        event = Event()
        event.mini_description = args['mini_description']
        event.description = args['description']
        event.create_date = datetime.now()
        event.create_user = args['create_user']
        event.num_likes = args['num_likes']
        session.add(event)
        session.commit()
        return jsonify({'id': event.id})

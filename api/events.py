from datetime import datetime

from flask import jsonify
from flask_restful import reqparse, abort, Resource

from data import db_session
from data.events import Event


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

    def post(self, event_id):  # редактирование события
        abort_if_event_not_found(event_id)
        session = db_session.create_session()
        event = session.query(Event).get(event_id)
        parser = reqparse.RequestParser()
        parser.add_argument('mini_description', required=True)
        parser.add_argument('description', required=True)
        args = parser.parse_args()

        events_args = ['mini_description', 'description']
        for arg in events_args:
            if args[arg] is not None:
                setattr(event, arg, args[arg])

        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, event_id):  # удаление события
        abort_if_event_not_found(event_id)
        session = db_session.create_session()
        event = session.query(Event).get(event_id)
        session.delete(event)
        session.commit()
        return jsonify({'success': 'OK'})


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
        args = parser.parse_args()
        session = db_session.create_session()
        event = Event()
        event.mini_description = args['mini_description']
        event.description = args['description']
        event.create_date = datetime.now()
        event.num_likes = 0
        event.create_user = args['create_user']
        session.add(event)
        session.commit()
        return jsonify({'id': event.id})

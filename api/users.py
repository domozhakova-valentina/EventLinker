from flask import jsonify
from flask_restful import reqparse, abort, Resource

from data import db_session
from data.users import User
from data.events import Event
from data.likes import Like
from data.comments import Comment


def get_metrics(user_id):
    session = db_session.create_session()
    num_events = session.query(Event).filter(Event.create_user == user_id).count()
    num_like_up = session.query(Like).filter(Like.user_id == user_id).count()
    events = session.query(Event).filter(Event.create_user == user_id).all()
    num_liked = 0
    for event in events:
        num_liked += session.query(Like).filter(Like.event_id == event.id).count()
    num_comments = session.query(Comment).filter(Comment.create_user == user_id).count()
    metrics = {"events": num_events, "like_up": num_like_up, "liked": num_liked,
               "comments": num_comments}  # данные-метрики из БД по пользователю
    return metrics


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):  # информации о конкретном пользователе
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        metrics = get_metrics(user_id)
        return jsonify(
            {'user': user.to_dict(only=('id', 'name', 'about', 'email', 'location', 'date_of_birth', 'user_type')),
             'metrics': metrics})

    def post(self, user_id):  # редактирование
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        parser = reqparse.RequestParser()
        parser.add_argument('user_type')
        parser.add_argument('name', required=True)
        parser.add_argument('about', required=True)
        parser.add_argument('location')
        parser.add_argument('date_of_birth')
        parser.add_argument('email', required=True)
        parser.add_argument('hashed_password', required=True)
        args = parser.parse_args()

        # Проверяем уникальность email
        if args['email']:
            if session.query(User).filter(User.email == args['email']).first():
                abort(400, message=f'User with this email already exists')

        user_args = ['user_type', 'name', 'about', 'location', 'date_of_birth', 'email']
        for arg in user_args:
            if args[arg] is not None:
                setattr(user, arg, args[arg])

        if args.get('hashed_password'):  # Если передан новый пароль
            user.set_password(args['hashed_password'])

        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, user_id):  # удаление пользователя
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):  # получение списка пользователей
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        users_list = []
        for user in users:
            metrics = get_metrics(user.id)  # Получаем метрики для пользователя
            user_dict = user.to_dict(only=('id', 'name', 'about', 'email', 'location', 'date_of_birth', 'user_type'))
            user_dict['metrics'] = metrics
            users_list.append(user_dict)  # Добавляем пользователя в список
        return jsonify({'users': users_list})

    def post(self):  # создание нового пользователя
        parser = reqparse.RequestParser()
        parser.add_argument('user_type', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('about', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('location')
        parser.add_argument('date_of_birth')
        parser.add_argument('hashed_password', required=True)
        args = parser.parse_args()
        db_sess = db_session.create_session()

        # Проверка на уникальность email
        if db_sess.query(User).filter(User.email == args['email']).first():
            abort(400, message=f'User with this email already exists')

        session = db_session.create_session()
        user = User()
        user_args = ['user_type', 'name', 'about', 'location', 'date_of_birth', 'email']
        for arg in user_args:
            if args[arg] is not None:
                setattr(user, arg, args[arg])
        user.set_password(args['hashed_password'])
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})

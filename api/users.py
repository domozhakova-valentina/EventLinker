from flask import jsonify
from flask_restful import reqparse, abort, Resource

from data import db_session
from data.users import User


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
        return jsonify({'user': user.to_dict(
            only=('id', 'name', 'about', 'email'))})

    def post(self, user_id):  # редактирование
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('about', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('hashed_password', required=True)
        args = parser.parse_args()

        # Проверяем уникальность email
        if args['email']:
            if User.query.filter_by(email=args['email']).first():
                abort(400, message=f'User with this email already exists')

        user_args = ['name', 'about', 'email', 'hashed_password']
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
        return jsonify(
            {
                'users':
                    [item.to_dict(only=('id', 'name', 'about', 'email'))
                     for item in users]
            }
        )

    def post(self):  # создание нового пользователя
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('about', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('hashed_password', required=True)
        args = parser.parse_args()

        # Проверка на уникальность email
        if User.query.filter_by(email=args['email']).first():
            abort(400, message=f'User with this email already exists')

        session = db_session.create_session()
        user = User()
        user.name = args['name']
        user.about = args['about']
        user.email = args['email']
        user.set_password(args['hashed_password'])
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})

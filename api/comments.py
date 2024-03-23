from datetime import datetime

from flask import jsonify
from flask_restful import reqparse, abort, Resource

from data import db_session
from data.comments import Comment


def abort_if_comment_not_found(comment_id):
    session = db_session.create_session()
    comment = session.query(Comment).get(comment_id)
    if not comment:
        abort(404, message=f"Comment {comment_id} not found")


class CommentResource(Resource):
    def get(self, comment_id):  # получение информации по комментарию
        abort_if_comment_not_found(comment_id)
        session = db_session.create_session()
        comment = session.query(Comment).get(comment_id)
        return jsonify({'comment': comment.to_dict(
            only=('id', 'text', 'create_date', 'create_user', 'event_id'))})

    def post(self, comment_id):  # обновление комментария
        abort_if_comment_not_found(comment_id)
        session = db_session.create_session()
        comment = session.query(Comment).get(comment_id)
        parser = reqparse.RequestParser()
        parser.add_argument('text', required=True)
        comment.text = parser.parse_args()['text']
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, comment_id):  # удаление комментария
        abort_if_comment_not_found(comment_id)
        session = db_session.create_session()
        comment = session.query(Comment).get(comment_id)
        session.delete(comment)
        session.commit()
        return jsonify({'success': 'OK'})


class CommentsListResource(Resource):
    def post(self):  # создание нового комментария
        parser = reqparse.RequestParser()
        parser.add_argument('text', required=True)
        parser.add_argument('create_user', required=True, type=int)
        parser.add_argument('event_id', required=True, type=int)
        args = parser.parse_args()
        session = db_session.create_session()
        comment = Comment()
        comment.text = args['text']
        comment.create_date = datetime.now()
        comment.create_user = args['create_user']
        comment.event_id = args['event_id']
        session.add(comment)
        session.commit()
        return jsonify({'id': comment.id})

import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'comment'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String)
    create_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    create_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    user = orm.relationship('User')

    event_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("event.id"))
    event = orm.relationship('Event')
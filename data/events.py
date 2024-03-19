import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy_imageattach.entity import Image, image_attachment
from .db_session import SqlAlchemyBase


class EventPicture(SqlAlchemyBase, Image):
    '''Класс для добавления изображений'''

    event_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('event.id'), primary_key=True)
    event = orm.relationship('Event')
    __tablename__ = 'event_picture'


class Event(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'event'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    photo = image_attachment('EventPicture')
    mini_description = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    create_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    num_likes = sqlalchemy.Column(sqlalchemy.Integer)

    create_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    user = orm.relationship('User')
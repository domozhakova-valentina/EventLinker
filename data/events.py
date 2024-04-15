import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Event(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'event'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    photo = sqlalchemy.Column(sqlalchemy.LargeBinary)
    event_type = sqlalchemy.Column(sqlalchemy.String)
    mini_description = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    create_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    num_likes = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    likes = orm.relationship("Like", back_populates='event', cascade='save-update, merge, delete')

    create_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    user = orm.relationship('User')

    comments = orm.relationship("Comment", back_populates='event', cascade='save-update, merge, delete')

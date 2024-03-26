from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
import sqlalchemy
from .db_session import SqlAlchemyBase

# Like = sqlalchemy.Table(
#     'likes_user_to_events',
#     SqlAlchemyBase.metadata,
#     sqlalchemy.Column('user', sqlalchemy.Integer,
#                       sqlalchemy.ForeignKey('user.id')),
#     sqlalchemy.Column('event', sqlalchemy.Integer,
#                       sqlalchemy.ForeignKey('event.id'))
# )


class Like(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'likes_user_to_events'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = Column('user', Integer, ForeignKey('user.id'))
    event_id = Column('event', Integer, ForeignKey('event.id'))

    user = relationship('User')
    event = relationship('Event')

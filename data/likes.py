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

    user_id = Column('user', Integer, ForeignKey('user.id'), primary_key=True)
    event_id = Column('event', Integer, ForeignKey('event.id'), primary_key=True)

    user = relationship('User')
    event = relationship('Event')

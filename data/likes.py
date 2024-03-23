from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

import sqlalchemy
from .db_session import SqlAlchemyBase

association_table = sqlalchemy.Table(
    'likes_user_to_events',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('user.id')),
    sqlalchemy.Column('event', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('event.id'))
)


class Like(SqlAlchemyBase):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    event_id = Column(Integer, ForeignKey('events.id'))

    user = relationship('User', backref='likes')
    event = relationship('Event', backref='likes')

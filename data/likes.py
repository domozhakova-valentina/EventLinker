import sqlalchemy
from .db_session import SqlAlchemyBase

association_table = sqlalchemy.Table(
    'likes_user_to_events',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('user.id')),
    sqlalchemy.Column('event', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('event.id')))

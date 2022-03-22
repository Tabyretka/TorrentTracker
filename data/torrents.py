import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from .tags import tags


class Torrents(SqlAlchemyBase):
    __tablename__ = 'torrents'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    pic_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    magnet = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    tags = orm.relationship('Tag', secondary=tags, backref=orm.backref('torrents', lazy='dynamic'))
    user = orm.relation('User')

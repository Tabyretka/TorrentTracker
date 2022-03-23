import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from .tags import tags


class Torrents(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'torrents'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    pic_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    magnet = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    tags = orm.relationship('Tag', secondary=tags, backref=orm.backref('torrents', lazy='dynamic'))
    comments = orm.relation("Comment", back_populates='torrent')

    def __repr__(self):
        return '<Torrent id: {}, name: {}>'.format(self.id, self.name)

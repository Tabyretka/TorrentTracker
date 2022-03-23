import sqlalchemy
from .db_session import SqlAlchemyBase

tags = sqlalchemy.Table(
    'tags',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('torrent_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('torrents.id')),
    sqlalchemy.Column('tag_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('tag.id'))
)


class Tag(SqlAlchemyBase):
    __tablename__ = 'tag'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return '<Tag id: {}, name: {}>'.format(self.id, self.name)

from data import db_session
from data.torrents import Torrents
from data.tags import Tag
from data.users import User

db_session.global_init("db/db.sqlite")
db_sess = db_session.create_session()

tag = Tag(name='фильмы')
db_sess.add(tag)
tag = Tag(name='сериалы')
db_sess.add(tag)
tag = Tag(name='софт')
db_sess.add(tag)
db_sess.commit()
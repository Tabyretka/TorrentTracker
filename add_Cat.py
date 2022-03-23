from data import db_session
from data.comments import Comment
from data.torrents import Torrents
from data.tags import Tag
from data.users import User


def create():
    db_session.global_init("db/db.sqlite")
    db_sess = db_session.create_session()

    tag = Tag(name='фильмы')
    db_sess.add(tag)

    tag = Tag(name='сериалы')
    db_sess.add(tag)

    tag = Tag(name='софт')
    db_sess.add(tag)

    db_sess.commit()


def zzz():
    db_session.global_init("db/db.sqlite")
    db_sess = db_session.create_session()
    tor = db_sess.query(Torrents).first()
    comment = Comment(text='zalupa', torrent=tor)
    db_sess.add(comment)
    db_sess.commit()
    db_sess.close()


create()

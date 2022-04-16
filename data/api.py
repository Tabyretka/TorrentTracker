import flask
from flask import jsonify
from . import db_session
from .torrents import Torrents

blueprint = flask.Blueprint(
    'api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api')
def api_index():
    return jsonify(
        {'api': [
            {'/api/torrents': 'will return a list of all torrents with information'},
            {'/api/torrents/<int:id>': 'will return information about a specific torrent'},
            {'/api/torrents/search/<q>': 'search for torrents by name, will return a list of results'}
        ]}
    )


@blueprint.route('/api/torrents')
def get_torrents():
    db_sess = db_session.create_session()
    torrents = db_sess.query(Torrents).all()
    return jsonify(
        {
            'torrents':
                [item.to_dict(only=('name', 'description', 'user.name', 'pic_url', 'magnet'))
                 for item in torrents]
        }
    )


@blueprint.route('/api/torrents/<int:id>')
def get_torrent(id):
    db_sess = db_session.create_session()
    torrent = db_sess.query(Torrents).filter(Torrents.id == id).first()
    if torrent:
        return jsonify(
            {
                'torrent':
                    torrent.to_dict(only=('name', 'description', 'user.name', 'pic_url', 'magnet'))
            }
        )
    else:
        return jsonify({'error': 'Not found'})


@blueprint.route('/api/torrents/search/<q>')
def search(q):
    db_sess = db_session.create_session()
    torrents = db_sess.query(Torrents).filter(Torrents.name.contains(q)).all()
    if torrents:
        return jsonify(
            {
                'torrents':
                    [item.to_dict(only=('name', 'description', 'user.name', 'pic_url', 'magnet'))
                     for item in torrents]
            }
        )
    else:
        return jsonify({'error': 'Not found'})

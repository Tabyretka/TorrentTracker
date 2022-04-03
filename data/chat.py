import flask

from . import db_session

blueprint = flask.Blueprint(
    'chat',
    __name__,
    template_folder='templates'
)


@blueprint.route('/chat')
def get_news():
    return flask.render_template('chat/index.html')

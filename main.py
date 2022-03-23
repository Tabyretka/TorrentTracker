import flask
import flask_login
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_simple_captcha import CAPTCHA
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from data import db_session
from data.login_form import LoginForm
from data.users import User
from data.register import RegisterForm
from data.comments_form import CommentForm
from data.comments import Comment
from data.torrents import Torrents
from data.add_torrent import AddTorrentForm
from data.tags import Tag

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
CAPTCHA = CAPTCHA(config={'SECRET_CAPTCHA_KEY': 'wMmeltW4mhwidorQRli6Oijuhygtfgybunxx9VPXldz'})
app = CAPTCHA.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)


class AdminView(ModelView):
    def is_accessible(self):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == flask_login.current_user.name).first()
        if user.type == 1:
            db_sess.close()
            return True
        db_sess.close()
        return False

    def inaccessible_callback(self, name, **kwargs):
        return flask.abort(404)


class HomeAdminView(AdminIndexView):
    def is_accessible(self):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == flask_login.current_user.name).first()
        if user.type == 1:
            db_sess.close()
            return True
        db_sess.close()
        return False

    def inaccessible_callback(self, name, **kwargs):
        return flask.abort(404)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            db_sess.close()
            return redirect("/")
        return render_template('login.html', message="Ошибка в логине или пароле", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/')
def index():
    q = request.args.get('q')
    db_sess = db_session.create_session()
    if q:
        torrents = db_sess.query(Torrents).filter(
            Torrents.name.contains(q)).all()
        db_sess.close()
        return render_template('torrents.html', torrents=torrents, title='Результаты поиска')
    else:
        torrents = db_sess.query(Torrents).all()
        db_sess.close()
        return render_template('torrents.html', torrents=torrents, title='Последние торренты')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    captcha = CAPTCHA.create()
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают", captcha=captcha)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже существует", captcha=captcha)
        c_hash = request.form.get('captcha-hash')
        c_text = request.form.get('captcha-text')
        if not CAPTCHA.verify(c_text, c_hash):
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Неверная каптча", captcha=captcha)

        all_users = db_sess.query(User).all()
        if all_users:
            user = User(
                name=form.name.data,
                age=form.age.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            db_sess.close()
            return redirect('/login')
        else:
            user = User(
                name=form.name.data,
                age=form.age.data,
                email=form.email.data,
                type=1
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            db_sess.close()
            return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, captcha=captcha)


@app.route('/addtorrent', methods=['GET', 'POST'])
@login_required
def addtorrent():
    add_form = AddTorrentForm()
    if add_form.validate_on_submit():
        db_sess = db_session.create_session()
        if add_form.pic_url.data != '':
            if 'https://pasteboard.co/' in add_form.pic_url.data:
                pic_url = f"https://gcdnb.pbrd.co/images/{add_form.pic_url.data.split('/')[-1]}"
            else:
                pic_url = add_form.pic_url.data
        else:
            pic_url = ''
        tag = request.form['Tags']
        tag = db_sess.query(Tag).filter(Tag.id == int(tag)).first()
        torrent = Torrents(
            name=add_form.name.data,
            description=add_form.description.data,
            user=flask_login.current_user,
            pic_url=pic_url,
            magnet=add_form.magnet.data
        )
        torrent.tags.append(tag)
        db_sess.add(torrent)
        db_sess.commit()
        db_sess.close()
        return redirect('/')
    db_sess = db_session.create_session()
    tags = db_sess.query(Tag).all()
    db_sess.close()
    return render_template('addtorrent.html', title='Добавление торрента', form=add_form, tags=tags)


@app.route('/torrents/<int:id>', methods=['GET', 'POST'])
def view_page(id):
    db_sess = db_session.create_session()
    torrent = db_sess.query(Torrents).filter(Torrents.id == id).first()
    if torrent:
        tags = torrent.tags
        comments = torrent.comments
        db_sess.close()
        return render_template('view_page.html', torrent=torrent, tags=tags, comms=comments, negr=int(id))
    else:
        db_sess.close()
        flask.abort(404)


@app.route('/add-comm/<int:id>', methods=['POST', 'GET'])
@login_required
def add_comm(id):
    form = CommentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        torrent = db_sess.query(Torrents).filter(Torrents.id == id).first()
        comment = Comment(text=form.comment.data, torrent=torrent, user_name=flask_login.current_user.name)
        db_sess.add(comment)
        db_sess.commit()
        db_sess.close()
        return redirect(f'/torrents/{id}')
    db_sess = db_session.create_session()
    torrent = db_sess.query(Torrents).filter(Torrents.id == id).first()
    if torrent:
        db_sess.close()
        return render_template('addcomment.html', form=form)
    else:
        db_sess.close()
        flask.abort(404)


@app.route('/my-torrents')
@login_required
def my_torrents():
    db_sess = db_session.create_session()
    torrents = db_sess.query(Torrents).filter(
        Torrents.user_id == flask_login.current_user.id)
    if torrents:
        return render_template('my_torrents.html', torrents=torrents, title='Мои торренты')
    else:
        return render_template('my_torrents.html', title='Мои торренты')


@app.route('/edit-torrent/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_torrent(id):
    form = AddTorrentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        torrent = db_sess.query(Torrents).filter(Torrents.id == id,
                                                 Torrents.user_id == flask_login.current_user.id).first()
        if torrent:
            form.name.data = torrent.name
            form.description.data = torrent.description
            form.pic_url.data = torrent.pic_url
            form.magnet.data = torrent.magnet
        else:
            flask.abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        torrent = db_sess.query(Torrents).filter(Torrents.id == id,
                                                 Torrents.user_id == flask_login.current_user.id).first()
        if torrent:
            torrent.name = form.name.data
            torrent.description = form.description.data
            torrent.pic_url = form.pic_url.data
            torrent.magnet = form.magnet.data
            db_sess.commit()
            db_sess.close()
            return redirect(f'/torrents/{id}')
        else:
            flask.abort(404)
    return render_template('addtorrent.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/delete-torrent/<int:id>')
@login_required
def delete_torrent(id):
    db_sess = db_session.create_session()
    torrent = db_sess.query(Torrents).filter(Torrents.id == id,
                                             Torrents.user_id == flask_login.current_user.id).first()
    if torrent:
        db_sess.delete(torrent)
        db_sess.commit()
        db_sess.close()
        return redirect('/my-torrents')
    else:
        flask.abort(404)
    return redirect('/')


@app.route('/tags/<name>')
def tags(name):
    db_sess = db_session.create_session()
    tag = db_sess.query(Tag).filter(Tag.name == name).first()
    torrents = tag.torrents.all()
    return render_template('torrents.html', torrents=torrents, title=f'Торренты с тегом "{tag.name}"')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


def main():
    db_session.global_init("db/db.sqlite")
    db_sess = db_session.create_session()
    admin = Admin(app, 'Torrent Tracker', url='/', index_view=HomeAdminView(name='home'))
    admin.add_views(AdminView(Torrents, db_sess), AdminView(Tag, db_sess), AdminView(User, db_sess),
                    AdminView(Comment, db_sess))
    app.run(debug=True, use_debugger=True, use_reloader=True)
    db_sess.close()


if __name__ == '__main__':
    main()

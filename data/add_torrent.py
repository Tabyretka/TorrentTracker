from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class AddTorrentForm(FlaskForm):
    name = StringField('Название торрента', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    pic_url = StringField('Ссылка на фото (брать на pasteboard.co)')
    magnet = StringField('Magnet-ссылка', validators=[DataRequired()])
    submit = SubmitField('Submit')

from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, URL

class MusicSubmitForm(Form):
    url = StringField('URL', validators=[DataRequired(), URL()])

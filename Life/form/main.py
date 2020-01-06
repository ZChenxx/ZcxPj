from flask_pagedown.fields import PageDownField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError

class PostForm(FlaskForm):
    body = PageDownField('mind',validators=[DataRequired()])
    submit = SubmitField('发布')
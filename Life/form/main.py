from flask_pagedown.fields import PageDownField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError

class PostForm(FlaskForm):
    body = PageDownField('mind',validators=[DataRequired()])
    submit = SubmitField('发布')


class CommentForm(FlaskForm):
    body = StringField('comment',validators=[DataRequired()])
    submit = SubmitField('发布')

class EditProfileForm(FlaskForm):
    username = StringField('用户名',validators=[Length(0,64)])
    location = StringField('位置',validators=[Length(0,64)])
    about_me = TextAreaField('个性签名')
    submit = SubmitField('确认修改')
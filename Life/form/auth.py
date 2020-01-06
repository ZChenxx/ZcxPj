

from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError

from Life.models import User

class RegisterForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Length(1,64)])
    username = StringField('Username',validators=[DataRequired(),Length(1,20),Regexp('^[a-zA-Z0-9]*$',message='用户名由字母和数字组成')])
    password = PasswordField('Password',validators=[DataRequired(),Length(8,128),EqualTo('password2')])
    password2 = PasswordField('Confirm',validators=[DataRequired()])
    submit = SubmitField('注册',render_kw={
            'class':"btn btn-lg btn-success btn-sm" ,
        }
)

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登陆',render_kw={'class':"btn btn-lg btn-info btn-sm"})
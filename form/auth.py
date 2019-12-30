

from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError

from models import User

class RegisterForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(1,30)])
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

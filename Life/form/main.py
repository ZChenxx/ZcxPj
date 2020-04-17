from flask_pagedown.fields import PageDownField
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, HiddenField, FileField,MultipleFileField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError

class PostForm(FlaskForm):
    body = PageDownField('mind',validators=[DataRequired()])
    photo = FileField('图片',render_kw={'class':"btn btn-success",'type':'file','id':'file','multiple':''})
    movie = FileField('电影')
    submit = SubmitField('发布')


class CommentForm(FlaskForm):
    body = StringField('comment',validators=[DataRequired()])
    submit = SubmitField('发布')

class EditProfileForm(FlaskForm):
    username = StringField('用户名',validators=[Length(0,64)])
    location = StringField('位置',validators=[Length(0,64)])
    about_me = TextAreaField('个性签名')
    submit = SubmitField('确认修改')

class UploadAvatarForm(FlaskForm):
    image = FileField('上传',validators=[FileRequired(),FileAllowed(['jpg','png'],'文件格式应该为.jpg或.png')])
    submit = SubmitField('上传')

class CropAvatarForm(FlaskForm):
    x = HiddenField()
    y = HiddenField()
    w = HiddenField()
    h = HiddenField()
    submit = SubmitField('裁剪并上传')
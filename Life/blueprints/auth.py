from flask import url_for, render_template, flash, Blueprint
from flask_login import current_user, login_user, login_required, logout_user
from Life.models import User
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from Life.form.auth import RegisterForm, LoginForm

auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        username = form.username.data
        password = form.password.data
        user = User()
        user.email = email
        user.username = username
        user.password_hash = generate_password_hash(password)

        if User.register(user):
            flash('注册成功','ok')
            return redirect(url_for('auth.register'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login/',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.validate_password(form.password.data):
            if login_user(user,form.remember_me.data):
                return redirect(url_for('main.index'))
            else:
                flash('登录失败','err')
                return redirect('login')
        flash('密码错误','err')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

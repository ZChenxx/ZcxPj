from flask import url_for, session, render_template, flash
from flask_login import current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from form.auth import RegisterForm
from models import User, db, app


@app.route('/',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data.lower()
        username = form.username.data
        password = form.password.data
        user = User(username=username,email=email,name=name,
                    password_hash=generate_password_hash(password))
        if User.register(user):
            flash('注册成功','ok')
            return redirect(url_for('register'))
    return render_template('auth/register.html',form=form)

app.run()
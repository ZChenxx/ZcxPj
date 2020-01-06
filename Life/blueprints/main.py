from flask import url_for, render_template, request, Blueprint
from flask_login import current_user
from werkzeug.utils import redirect

from Life.form.main import PostForm
from Life.models import db, Post

main_bp = Blueprint('main',__name__)

@main_bp.route('/',methods=['GET','POST'])
def index():
    form = PostForm()
    if current_user.is_authenticated and form.validate_on_submit():
        post = Post(body=form.body.data,author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    # page = request.args.get('page',1,type=int)
    return render_template('main/index.html', form=form,posts=posts)
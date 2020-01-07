from flask import url_for, render_template, request, Blueprint, flash
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from Life.form.main import PostForm, CommentForm
from Life.models import db, Post, Comment

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

@main_bp.route('/post/<int:id>',methods=['GET','POST'])
@login_required
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,post=post,author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('评论成功')
        return redirect(url_for('main.post',id=post.id))
    comments = Comment.query.filter_by(post_id=id).order_by(Comment.timestamp.desc()).all()
    return render_template('main/post.html',post=post,form=form,comments=comments)
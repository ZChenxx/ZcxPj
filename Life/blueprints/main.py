from flask import url_for, render_template, request, Blueprint, flash
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from Life.form.main import PostForm, CommentForm
from Life.models import db, Post, Comment, User

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

@main_bp.route('/post/<int:id>/edit',methods=['GET','POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        return  redirect(url_for('main.post',id=post.id))
    form.body.data = post.body
    return render_template('main/edit_post.html',form=form)

@main_bp.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('main/user.html',user=user,posts=posts)


@main_bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if current_user.is_following(user):
        flash('你已经关注过了','err')
        return redirect(url_for('main.user',username=username))
    current_user.follow(user)
    db.session.commit()
    flash('关注成功','ok')
    return redirect(url_for('main.user',username=username))

@main_bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if not current_user.is_following(user):
        flash('未关注此用户','err')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('已取消关注','ok')
    return redirect(url_for('main.user', username=username))


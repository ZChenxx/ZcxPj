import os

from flask import url_for, render_template, request, Blueprint, flash, make_response, send_from_directory, current_app
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from Life import avatars
from Life.form.main import PostForm, CommentForm, EditProfileForm, UploadAvatarForm, CropAvatarForm
from Life.models import db, Post, Comment, User, Follow, Photo, Movie
from utils import rename_image,resize_photo

main_bp = Blueprint('main',__name__)

@main_bp.route('/',methods=['GET','POST'])
def index():
    form = PostForm()
    if current_user.is_authenticated and form.validate_on_submit():
        post = Post(body=form.body.data,author=current_user._get_current_object())
        db.session.add(post)
        db.session.flush()       #获取插入的id
        post_id = post.id
        db.session.commit()
        print(request.files)
        if form.photo.data.filename:
            for f in request.files.getlist('photo'):
                filename = rename_image(f.filename)
                print(filename)
                f.save(os.path.join(current_app.config['PHOTO_UPLOAD_PATH'], filename))
                s_filename = resize_photo(filename)
                photo = Photo(filename=filename,filename_s=s_filename,author=current_user._get_current_object(),post_id=post_id)
                db.session.add(photo)
                db.session.commit()
        if form.movie.data.filename:
            f = request.files.get('movie')
            filename = rename_image(f.filename)
            print(filename)
            f.save(os.path.join(current_app.config['MOVIE_UPLOAD_PATH'],filename))
            movie = Movie(filename=filename,author=current_user._get_current_object(),post_id=post_id)
            db.session.add(movie)
            db.session.commit()
        return redirect(url_for('main.index'))
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed',''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    posts = query.order_by(Post.timestamp.desc())
    photos = Photo.query.all()
    movies = Movie.query.all()
    return render_template('main/index.html', show_followed=show_followed,form=form,posts=posts,photos=photos,movies=movies)

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
    photos = Photo.query.all()
    movies = Movie.query.all()
    return render_template('main/post.html',post=post,form=form,comments=comments,photos=photos,movies=movies)

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

@main_bp.route('/post/<int:id>/delete',methods=['GET'])
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    user = User.query.filter_by(id=post.author_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.user',username=user.username))

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

@main_bp.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.location =form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        return redirect(url_for('main.user',username=current_user.username))
    form.username.data = current_user.username
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('main/edit_profile.html',form=form)

@main_bp.route('/edit_profile/avatar',methods=['POST','GET'])
@login_required
def change_avatar():
    upload_form = UploadAvatarForm()
    crop_form = CropAvatarForm()
    return render_template('main/change_avatar.html',upload_form=upload_form,crop_form=crop_form)

@main_bp.route('/edit_profile/avatar/upload',methods=['POST'])
@login_required
def upload_avatar():
    form = UploadAvatarForm()
    if form.validate_on_submit():
        image = form.image.data
        filename = avatars.save_avatar(image)
        current_user.avatar_raw = filename
        db.session.commit()
    return redirect(url_for('main.change_avatar'))

@main_bp.route('/edit_profile/avatar/crop',methods=['POST'])
@login_required
def crop_avatar():
    form = CropAvatarForm()
    if form.validate_on_submit():
        x = form.x.data
        y = form.y.data
        w = form.w.data
        h = form.h.data
        filenames = avatars.crop_avatar(current_user.avatar_raw,x,y,w,h)
        current_user.avatar_s = filenames[0]
        current_user.avatar_m = filenames[1]
        current_user.avatar_l = filenames[2]
        db.session.commit()
    return redirect(url_for('main.edit_profile'))


@main_bp.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    pagination = user.followers.paginate(1,1,error_out=False)
    follows = [{'user':item.follower,'timestamp':item.timestamp} for item in pagination.items]
    return render_template('main/followers.html',user=user,follows=follows)

@main_bp.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    pagination = user.followed.paginate(1,1,error_out=False)
    follows = [{'user':item.followed,'timestamp':item.timestamp} for item in pagination.items]
    return render_template('main/followers.html',user=user,follows=follows)

@main_bp.route('/all')
@login_required
def show_all():
    res = make_response(redirect(url_for('main.index')))
    res.set_cookie('show_followed','',max_age=30*24*60*60)
    return res


@main_bp.route('/followed')
@login_required
def show_followed():
    res = make_response(redirect(url_for('main.index')))
    res.set_cookie('show_followed','1',max_age=30*24*60*60)
    return res


@main_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'],filename)

@main_bp.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'POST' and 'file' in request.files:
        f = request.files.get('file')
        filename = rename_image(f.filename)
        f.save(os.path.join(current_app.config['PHOTO_UPLOAD_PATH'], filename))
        # filename_s = resize_image(f, filename, current_app.config['ALBUMY_PHOTO_SIZE']['small'])
        # filename_m = resize_image(f, filename, current_app.config['ALBUMY_PHOTO_SIZE']['medium'])
        photo = Photo(
            filename=filename,
            # filename_s=filename_s,
            # filename_m=filename_m,
            author=current_user._get_current_object()
        )
        db.session.add(photo)
        db.session.commit()
    return render_template('main/upload.html')
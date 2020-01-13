from datetime import datetime

from flask import current_app
from flask_login import  UserMixin
from werkzeug.security import check_password_hash

from . import db,login_manager

class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    followed_id = db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,index=True)
    email = db.Column(db.String(254),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    website = db.Column(db.String(255),default=None)
    location = db.Column(db.String(50),default=None)
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime,default=datetime.now())
    confirmed = db.Column(db.Boolean,default=False)
    last_seen = db.Column(db.DateTime(),default=datetime.utcnow)
    posts = db.relationship('Post',backref='author',lazy='dynamic')
    active = db.Column(db.Boolean,default=True)
    comments = db.relationship('Comment',backref='author',lazy='dynamic')
    followed = db.relationship('Follow',foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower',lazy='joined'),lazy='dynamic',
                               cascade='all,delete-orphan')
    followers = db.relationship('Follow',foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed',lazy='joined'),lazy='dynamic',
                                cascade='all,delete-orphan')

    def register(user):
        try:
            db.session.add(user)
            db.session.commit()
            return True
        except Exception:
            return False

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return self.active

    def follow(self,user):
        if not self.is_following(user):
            f = Follow(follower=self,followed=user)
            db.session.add(f)

    def unfollow(self,user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self,user):
        return self.followed.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self,user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow,index=True)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    comments = db.relationship('Comment',backref='post',lazy='dynamic')

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))




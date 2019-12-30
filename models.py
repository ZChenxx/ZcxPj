from datetime import datetime
from logging import DEBUG

import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import UserMixin, LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zcx1203@localhost/Life'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


app.config['SECRET_KEY'] = 'zcx1203'


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,index=True)
    email = db.Column(db.String(254),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))
    website = db.Column(db.String(255),default=None)
    bio = db.Column(db.String(120),default=None)
    location = db.Column(db.String(50),default=None)
    member_since = db.Column(db.DateTime,default=datetime.now())
    confirmed = db.Column(db.Boolean,default=False)

    def register(user):
        try:
            db.session.add(user)
            db.session.commit()
            return True
        except Exception:
            return False

# db.drop_all()
# db.create_all()


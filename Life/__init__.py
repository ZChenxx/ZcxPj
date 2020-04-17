import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager,AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_moment import Moment
from flask_avatars import Avatars
from flask_dropzone import Dropzone
from manage import config

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
avatars = Avatars()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
dropzone = Dropzone()

@login_manager.user_loader
def load_user(user_id):
    from Life.models import User
    user = User.query.get(int(user_id))
    return user


class Guest(AnonymousUserMixin):

    def can(self,permission_name):
        return False

    @property
    def is_admin(self):
        return False

login_manager.anonymous_user = Guest

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG','development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app._static_folder = 'static'
    register_extensions(app)
    register_blueprints(app)

    return app

def register_extensions(app):
    bootstrap.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)
    avatars.init_app(app)
    dropzone.init_app(app)

def register_blueprints(app):
    from Life.blueprints.auth import auth_bp
    from Life.blueprints.main import main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp,url_prefix='/auth')



app = create_app(os.getenv('FLASK_CONFIG','development'))

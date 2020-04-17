

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY','secret string')
    UPLOAD_PATH = os.path.join(basedir, 'Life/static')
    AVATARS_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    AVATARS_SAVE_PATH = os.path.join(AVATARS_UPLOAD_PATH, 'avatars')
    AVATARS_SIZE_TUPLE = (30, 100, 200)
    DROPZONE_MAX_SIZE = 3
    DROPZONE_MAX_FILES = 30
    DROPZONE_ALLOWED_FILE_TYPE = 'default'
    DROPZONE_ENABLE_CSRF = True
    PHOTO_UPLOAD_PATH = os.path.join(UPLOAD_PATH,'photos')
    MOVIE_UPLOAD_PATH = os.path.join(UPLOAD_PATH,'movies')
    ALBUMY_PHOTO_SIZE = {'small': 400,
                         'medium': 800}
    ALBUMY_PHOTO_SUFFIX = {
        ALBUMY_PHOTO_SIZE['small']: '_s',  # thumbnail
        ALBUMY_PHOTO_SIZE['medium']: '_m',  # display
    }


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:971203@localhost/Life'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

config = {
    'development': DevelopmentConfig,
}






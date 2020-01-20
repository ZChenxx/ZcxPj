

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY','secret string')
    UPLOAD_PATH = os.path.join(basedir, 'uploads')
    AVATARS_SAVE_PATH = os.path.join(UPLOAD_PATH, 'avatars')
    AVATARS_SIZE_TUPLE = (30, 100, 200)

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:zcx1203@localhost/Life'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

config = {
    'development': DevelopmentConfig,
}






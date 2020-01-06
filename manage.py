

import os


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY','secret string')

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:zcx1203@localhost/Life'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

config = {
    'development': DevelopmentConfig,
}






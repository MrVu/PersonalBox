import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET') or 'Vu1781991'

    @staticmethod
    def init_app(app):
        pass
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE') or 'sqlite:///'+ os.path.join(basedir,'data-dev.sqlite')
config = {'development': DevelopmentConfig, 'default': DevelopmentConfig}


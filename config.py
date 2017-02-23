import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET') or 'Whatever123`'
    SERVER_DOMAIN= os.environ.get('SERVER_DOMAIN') or "127.0.0.1:8000"

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    DEBUG= False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


config = {'development': DevelopmentConfig,
          'production': ProductionConfig,
          'default': DevelopmentConfig}

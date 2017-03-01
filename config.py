import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET') or 'Whatever123`'
    SERVER_DOMAIN = os.environ.get('SERVER_DOMAIN') or "127.0.0.1:8000"

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        syslog_handler = logging.FileHandler('Ubox.log')
        syslog_handler.setLevel(logging.WARNING)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        syslog_handler.setFormatter(formatter)
        app.logger.addHandler(syslog_handler)


config = {'development': DevelopmentConfig,
          'production': ProductionConfig,
          'unix': UnixConfig,
          'default': DevelopmentConfig}

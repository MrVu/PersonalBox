import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET') or 'Whatever123`'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Ubox]'
    FLASKY_MAIL_SENDER = 'Ubox Admin <admin@ubox.technology>'
    UBOX_ADMIN = os.environ.get('UBOX_ADMIN')
    SERVER_NAME = os.environ.get('SERVER_NAME') or "127.0.0.1:5000"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.UBOX_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.WARNING)
        app.logger.addHandler(mail_handler)


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class UnixConfig(ProductionConfig):
    COMPRESS_MIMETYPES = ['text/html',
                          'text/css',
                          'text/xml',
                          'application/json',
                          'application/javascript'
                          ]

    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500
    COMPRESS_REGISTER = True

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

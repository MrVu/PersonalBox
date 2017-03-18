from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import config, Config
from flask_login import LoginManager
from flask_mail import Mail
from flask_compress import Compress
from celery import Celery

db = SQLAlchemy()
mail = Mail()
compress = Compress()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # init app here
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    compress.init_app(app)
    celery.conf.update(app.config)

    # Register Blueprint
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from share import share as share_blueprint
    app.register_blueprint(share_blueprint)

    return app

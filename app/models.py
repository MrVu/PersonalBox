from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from functions import GetBasePath
from files import get_folder_size


class Shared(db.Model):
    __tablename__ = 'shared'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String)
    file_url = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64))
    userkey = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    shared_file = db.relationship('Shared', backref='user')
    storage = db.Column(db.Float)
    storage_used = db.Column(db.Float)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.storage is None:
            self.storage = 10 * 1024 * 1024 * 1024
        if self.storage_used is None:
            self.storage_used = 0
        db.session.add(self)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirm_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    @classmethod
    def token_load(cls, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        user_id = data.get('confirm')
        return user_id

    @classmethod
    def confirm(cls, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        id = data.get('confirm')
        user = User.query.get(id)
        if user is not None:
            user.confirmed = True
            db.session.add(user)
            db.session.commit()
            return True
        return False

    @classmethod
    def refix_used_storage(cls):
        users = User.query.all()
        for user in users:
            path = GetBasePath(user.userkey)
            folder_size = get_folder_size(path)
            user.storage_used = folder_size
            db.session.add(user)
            db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

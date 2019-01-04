from datetime import datetime

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from . import db


# 定义权限常量 ?为什么定义类 或许方便其他模块调用
class Permission(object):
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    default = db.Column(db.Boolean, default=False, index=True)
    permission = db.Column(db.Integer, default=0)

    def hash_permission(self, per):
        return self.permission & per == per  # 说明此权限存在

    def add_permission(self, per):
        if not self.hash_permission(per):
            self.permission |= per

    def remove_permission(self, per):
        if self.hash_permission(per):
            self.permission &= ~per

    def reset_permission(self):
        self.permission = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
            'Administrtor': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE,
                             Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
                db.session.add(role)
            print(role)
            role.reset_permission()
            for per in roles[r]:
                role.add_permission(per)
            role.default = default_role == r
        db.session.commit()

        def __repr__(self):
            return '<Role %r>' % self.name


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    qq_account = db.Column(db.String(12))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email == current_app.config['ADMIN_EMAIL']:
            self.role = Role.query.filter_by(name='Administrator').first()
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    def can(self, per):
        return self.role is not None and self.role.hash_permission(per)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def generate_confirmed_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        token = s.dumps({'confirm': self.id}).decode('utf-8')
        return token

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_password_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def password_reset(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if not user:
            return False
        user.password = new_password
        return True

    def generate_email_token(self, email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'user_id': self.id, 'new_email': email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        if self.id != data.get('user_id'):
            return False

        new_email = data.get('new_email')
        if new_email is None:
            return False
        else:
            if User.query.filter_by(email=new_email).first():
                return False
            else:
                self.email = new_email
                return True

    @property
    def password(self):
        raise AttributeError('不可读出密码')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def ping(self):
        self.last_seen = datetime.utcnow()

    def __repr__(self):
        return "<User %r>" % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, per):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False, nullable=False, index=True)
    is_active_flag = db.Column('is_active', db.Boolean, default=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    last_login = db.Column(db.DateTime)

    chats = db.relationship('Chat', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    posts = db.relationship('BlogPost', backref='author', lazy='dynamic')

    # Flask-Login override: use our own is_active_flag so a disabled user
    # can't be logged in by the framework either.
    @property
    def is_active(self):
        return self.is_active_flag

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def chat_count(self):
        return self.chats.count()

    def update_last_login(self):
        self.last_login = datetime.now(timezone.utc)

    def __repr__(self):
        return f'<User {self.username}>'
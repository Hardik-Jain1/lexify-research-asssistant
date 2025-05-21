# app/models/user.py
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False) # Increased length for stronger hashes
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Relationships
    chat_sessions = db.relationship('ChatSession', back_populates='user', lazy='dynamic', cascade="all, delete-orphan")
    # If you want to track which user uploaded/processed which paper:
    # papers_processed = db.relationship('PaperMetadata', back_populates='processed_by_user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
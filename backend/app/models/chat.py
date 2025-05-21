# app/models/chat.py
from app.extensions import db
import datetime

class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_name = db.Column(db.String(200), nullable=True, default=lambda: f"Chat Session - {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')}") # Optional name
    created_at = db.Column(db.DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

    user = db.relationship('User', back_populates='chat_sessions')
    messages = db.relationship('ChatMessage', back_populates='session', lazy='dynamic', cascade="all, delete-orphan", order_by="ChatMessage.timestamp")

    # Many-to-many relationship with papers involved in this chat session
    papers_in_session = db.relationship('PaperMetadata', secondary='chat_session_papers', lazy='dynamic',
                                        backref=db.backref('chat_sessions', lazy='dynamic'))

    def __repr__(self):
        return f'<ChatSession {self.id} by User {self.user_id}>'

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_sessions.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), index=True)
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    
    # Optional: Store context or sources used for assistant's response
    # sources_json = db.Column(db.JSON, nullable=True) # Store the 'sources' dict from chat_with_papers
    # token_usage_json = db.Column(db.JSON, nullable=True) # Store token usage

    session = db.relationship('ChatSession', back_populates='messages')

    def __repr__(self):
        return f'<ChatMessage {self.id} ({self.role}) at {self.timestamp}>'

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "timestamp": self.timestamp.isoformat(),
            "role": self.role,
            "content": self.content
            # "sources": self.sources_json if self.sources_json else None,
            # "token_usage": self.token_usage_json if self.token_usage_json else None
        }
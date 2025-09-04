from app.extensions import db
import datetime

# Association table for many-to-many relationship between ChatSession and PaperMetadata
chat_session_papers = db.Table('chat_session_papers',
    db.Column('chat_session_id', db.Integer, db.ForeignKey('chat_sessions.id'), primary_key=True),
    db.Column('paper_metadata_id', db.Integer, db.ForeignKey('paper_metadata.id'), primary_key=True)
)

class PaperMetadata(db.Model):
    __tablename__ = 'paper_metadata'

    id = db.Column(db.Integer, primary_key=True)
    arxiv_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    title = db.Column(db.String(500), nullable=False)
    authors = db.Column(db.JSON)
    abstract = db.Column(db.Text)
    published_date = db.Column(db.Date)
    pdf_url = db.Column(db.String(500))
    entry_id = db.Column(db.String(200))
    source = db.Column(db.String(50), default="arXiv")

    # Local storage and processing status
    local_pdf_path = db.Column(db.String(500), nullable=True)
    downloaded_at = db.Column(db.DateTime, nullable=True)
    text_extracted_at = db.Column(db.DateTime, nullable=True)
    cleaned_text_at = db.Column(db.DateTime, nullable=True)
    indexed_at = db.Column(db.DateTime, nullable=True)
    qdrant_collection_name = db.Column(db.String(200), nullable=True, unique=True)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<PaperMetadata {self.arxiv_id} - {self.title[:50]}>'
import uuid
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

class Memo(db.Model):
    __tablename__ = 'memos'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    priority = db.Column(db.String(10), nullable=True)  # 重要度（high, medium, low）
    

 
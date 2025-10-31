from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ContentItem(db.Model):
    __tablename__ = 'content_items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)  # 'caption', 'post', 'thread', 'meme', 'reel'
    platform = db.Column(db.String(50), nullable=False)  # 'instagram', 'tiktok', 'x', 'facebook', etc.
    content_text = db.Column(db.Text, nullable=True)
    media_url = db.Column(db.String(500), nullable=True)
    hashtags = db.Column(db.Text, nullable=True)
    call_to_action = db.Column(db.String(200), nullable=True)
    source_material = db.Column(db.String(500), nullable=True)  # Reference to original content
    status = db.Column(db.String(20), default='draft')  # 'draft', 'approved', 'scheduled', 'published'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content_type': self.content_type,
            'platform': self.platform,
            'content_text': self.content_text,
            'media_url': self.media_url,
            'hashtags': self.hashtags,
            'call_to_action': self.call_to_action,
            'source_material': self.source_material,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ContentTemplate(db.Model):
    __tablename__ = 'content_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    template_text = db.Column(db.Text, nullable=False)
    variables = db.Column(db.Text, nullable=True)  # JSON string of template variables
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'content_type': self.content_type,
            'platform': self.platform,
            'template_text': self.template_text,
            'variables': self.variables,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class GenerationRequest(db.Model):
    __tablename__ = 'generation_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    request_type = db.Column(db.String(50), nullable=False)  # 'generate', 'repurpose'
    prompt = db.Column(db.Text, nullable=False)
    source_content = db.Column(db.Text, nullable=True)
    target_platform = db.Column(db.String(50), nullable=True)
    target_format = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'processing', 'completed', 'failed'
    result_content_id = db.Column(db.Integer, db.ForeignKey('content_items.id'), nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    result_content = db.relationship('ContentItem', backref='generation_request')
    
    def to_dict(self):
        return {
            'id': self.id,
            'request_type': self.request_type,
            'prompt': self.prompt,
            'source_content': self.source_content,
            'target_platform': self.target_platform,
            'target_format': self.target_format,
            'status': self.status,
            'result_content_id': self.result_content_id,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }


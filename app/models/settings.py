from app import db

from app.models.base import TABLE_ARGS

class SocialLink(db.Model):
    __tablename__ = 'social_links'
    __table_args__ = TABLE_ARGS
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(50))  # Имя иконки (например, 'facebook', 'instagram')
    is_active = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<SocialLink {self.name}>'

class SiteSettings(db.Model):
    __tablename__ = 'site_settings'
    __table_args__ = TABLE_ARGS
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text)
    
    # Поля для многоязычности
    value_uk = db.Column(db.Text)
    value_de = db.Column(db.Text)
    value_en = db.Column(db.Text)
    
    def __repr__(self):
        return f'<SiteSettings {self.key}>'
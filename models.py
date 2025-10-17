from app import db
from datetime import datetime

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    login_id = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uploader_type = db.Column(db.String(20))  # admin or school
    class_name = db.Column(db.String(20))
    subject = db.Column(db.String(100))
    chapter = db.Column(db.String(100))
    file_name = db.Column(db.String(255))
    file_url = db.Column(db.String(500))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

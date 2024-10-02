from os import getenv
from flask import Flask
from app import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app.config["SQLALCHEMY_DATABASE_URI"] =  "postgresql:///postgres"
app.config["DEBUG"] = True
db = SQLAlchemy(app)

"""class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.Integer, nullable=False)

    # Define relationship with BlogPost
    posts = db.relationship('BlogPost', backref='author', lazy=True)

class BlogPost(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
"""
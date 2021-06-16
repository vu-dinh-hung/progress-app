"""This script initializes the database"""
from main import db, create_app

app = create_app('development')

with app.app_context():
    db.create_all()

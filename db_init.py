"""This script initializes the database"""
from run import app
from main import db
from main.models.user import User
from main.models.habit import Habit
from main.models.log import Log

with app.app_context():
    db.create_all()

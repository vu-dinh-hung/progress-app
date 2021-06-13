'''Module for initializing the Flask application'''
from flask import Flask
from config import config
from main.db import db
from main.models.user import User


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)

    # routes
    @app.route('/hello/<name>')
    def greet(name):
        user = User(username=name, passwordHash='random')
        user.save()
        return User.find_by_username(name).to_dict()

    return app

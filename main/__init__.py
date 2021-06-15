'''Module for initializing the Flask application'''
from flask import Flask
from flask_jwt_extended import JWTManager
from main.config import config
from main.db import db
from main.controllers.user_router import user_router
from main.controllers.habit_router import habit_router
from main.controllers.log_router import log_router

jwt = JWTManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    jwt.init_app(app)

    # routes
    prefix = '/api'
    app.register_blueprint(user_router, url_prefix=prefix)
    app.register_blueprint(habit_router, url_prefix=prefix)
    app.register_blueprint(log_router, url_prefix=prefix)

    return app

"""Module for initializing the Flask application"""
import logging
from flask import Flask, request
from flask_jwt_extended import JWTManager
from main.config import config
from main.db import db
from main.controllers.user import user_router
from main.controllers.habit import habit_router
from main.controllers.log import log_router
from main.utils.logger import logger
from main.utils.error_handler import error_handler

jwt = JWTManager()


def create_app(config_name):
    """Return initialized and configured Flask app"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    jwt.init_app(app)

    # logging
    level = logging.INFO
    if config_name == "development":
        level = logging.DEBUG
    if config_name == "testing":
        level = logging.CRITICAL
    logger.setLevel(level)

    @app.after_request
    def log_request(response):
        logger.info(
            "%s %s %s : %s",
            request.remote_addr,
            request.method,
            request.full_path,
            response.status,
        )
        return response

    # error handling
    app.register_blueprint(error_handler)

    # routes
    prefix = "/api"
    app.register_blueprint(user_router, url_prefix=prefix)
    app.register_blueprint(habit_router, url_prefix=prefix)
    app.register_blueprint(log_router, url_prefix=prefix)

    return app

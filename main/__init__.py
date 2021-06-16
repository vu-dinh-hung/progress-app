"""Module for initializing the Flask application"""
import logging
from flask import Flask, request
from flask_jwt_extended import JWTManager
from main.config import config
from main.db import db
from main.controllers.user_router import user_router
from main.controllers.habit_router import habit_router
from main.controllers.log_router import log_router
from main.utils.logger import logger
from main.utils.error_handlers import handle_exceptions

jwt = JWTManager()


def create_app(config_name):
    """Return initialized and configured Flask app"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    jwt.init_app(app)

    # set up logging
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

    app.register_error_handler(500, handle_exceptions)

    # routes
    prefix = "/api"
    app.register_blueprint(user_router, url_prefix=prefix)
    app.register_blueprint(habit_router, url_prefix=prefix)
    app.register_blueprint(log_router, url_prefix=prefix)

    return app

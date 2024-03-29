"""Module for initializing the Flask application"""
from flask import Flask
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException
from main.config import config
from main.db import db
from main.controllers.user import user_router
from main.controllers.habit import habit_router
from main.controllers.log import log_router
from main.exceptions import BadRequestError, UnauthorizedError, NotFoundError
from main.utils.logger import init_logger
from main.utils.error_handlers import (
    handle_http_errors,
    handle_exceptions,
    handle_bad_request,
    handle_not_found,
    handle_unauthorized,
)

jwt = JWTManager()


def create_app(config_name: str):
    """Return initialized and configured Flask app"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    jwt.init_app(app)

    # logging
    init_logger(app)

    # error handling
    app.register_error_handler(Exception, handle_exceptions)
    app.register_error_handler(HTTPException, handle_http_errors)
    app.register_error_handler(BadRequestError, handle_bad_request)
    app.register_error_handler(UnauthorizedError, handle_unauthorized)
    app.register_error_handler(NotFoundError, handle_not_found)

    # routes
    prefix = "/api"
    app.register_blueprint(user_router, url_prefix=prefix)
    app.register_blueprint(habit_router, url_prefix=prefix)
    app.register_blueprint(log_router, url_prefix=prefix)

    return app

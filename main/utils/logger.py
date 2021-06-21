"""Module for LogSetup class"""
from logging.config import dictConfig


def init_logger(app):
    """Initialize app logger with app.config"""
    log_level = app.config["LOG_LEVEL"]
    log_config = {
        "version": 1,
        "formatters": {
            "default": {
                "format": "%(asctime)s %(levelname)s: %(message)s",
            }
        },
        "handlers": {
            "rotating_file": {
                "level": log_level,
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "app.log",
                "backupCount": 4,
                "maxBytes": 100000,
                "formatter": "default",
                "delay": True,
            }
        },
        "root": {"handlers": ["rotating_file"]},
    }

    dictConfig(log_config)

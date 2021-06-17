"""Module for config class to store app variables"""
import os
import datetime
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base Config class"""

    SECRET_KEY = os.environ.get("SECRET_KEY", "defaulthardtoguessstring")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Config class for development"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL", "sqlite:///db_dev.sqlite"
    )
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)


class TestingConfig(Config):
    """Config class for testing"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL", "sqlite://")


class ProductionConfig(Config):
    """Config class for production"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///db.sqlite")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

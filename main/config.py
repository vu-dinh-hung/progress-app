"""Module for config class to store app variables"""
import os
import datetime
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base Config class"""

    SECRET_KEY = os.environ.get("SECRET_KEY", "defaulthardtoguessstring")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    """Config class for development"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL", "sqlite:///db_dev.sqlite"
    )
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)


class TestConfig(Config):
    """Config class for testing"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL", "sqlite://")


class ProdConfig(Config):
    """Config class for production"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "db.sqlite")


config = {
    "development": DevConfig,
    "testing": TestConfig,
    "production": ProdConfig,
    "default": DevConfig,
}

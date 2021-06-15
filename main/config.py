import os
import datetime

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'defaulthardtoguessstring')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL', 'sqlite:///db_dev.sqlite')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', 'sqlite://')


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'db.sqlite')


config = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig,

    'default': DevConfig
}

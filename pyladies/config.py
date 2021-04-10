import os

from app.utils import import_class


basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_API_CLASS = os.environ.get('DATABASE_API_CLASS') or \
                           'app.sqldb.MySQLDatabaseAPI'

    @classmethod
    def init_app(cls, app):
        app.db_api_class = import_class(cls.DATABASE_API_CLASS)


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    LOGIN_DISABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')


class Test2Config(Config):
    DEBUG = True
    TESTING = True
    LOGIN_DISABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


config = {
    'test': TestConfig,
    'test2': Test2Config,
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

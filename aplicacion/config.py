"""
Module configuration
"""
from aplicacion.secrets import SecretsDev


class Config(object):
    """
    Base configurations
    """
    SECRET_KEY = ''
    DEBUG = False


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    secrets_dev = SecretsDev()
    SQLALCHEMY_DATABASE_URI = secrets_dev.SQLALCHEMY_DATABASE_URI
    DEBUG = secrets_dev.DEBUG
    SQLALCHEMY_ECHO = secrets_dev.SQLALCHEMY_ECHO
    CACHE_TYPE = secrets_dev.CACHE_TYPE
    CACHE_REDIS_HOST = secrets_dev.CACHE_REDIS_HOST
    CACHE_REDIS_PORT = secrets_dev.CACHE_REDIS_PORT
    CACHE_REDIS_DB = secrets_dev.CACHE_REDIS_DB
    JWT_SECRET_KEY = secrets_dev.JWT_SECRET_KEY
    JWT_LIFETIME_HOURS = secrets_dev.JWT_LIFETIME_HOURS


class TestingConfig(Config):
    """
    Testing configurations
    """
    SQLALCHEMY_DATABASE_URI = ''
    TESTING = True


class ProductionConfig(Config):
    """
    Production configurations
    """


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

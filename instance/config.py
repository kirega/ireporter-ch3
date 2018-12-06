import os


class Config():
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = 'jwt-secret-string'
    DB_HOST = os.environ.get('DB_HOST')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASS = os.environ.get('DB_PASS')
    DB_NAME = os.environ.get('DB_NAME')
    DB_PORT = os.environ.get('DB_PORT')


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"


class TestingConfig(Config):
    TESTING = True
    DB_NAME = os.environ.get('DB_NAME_TEST')


settings = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}

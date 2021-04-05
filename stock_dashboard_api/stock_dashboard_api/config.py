import os


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = False
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_ENABLED = False

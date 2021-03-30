import os
from dotenv import load_dotenv

project_folder = os.path.expanduser('~/StockDashboard/StockDashboardAPI')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    RABBITMQ_CONNECTION_HOST = os.getenv('RABBITMQ_CONNECTION_HOST')
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    MAIL_HOST = os.getenv('MAIL_HOST')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')


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

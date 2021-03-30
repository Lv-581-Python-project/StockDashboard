import os
from dotenv import load_dotenv

project_folder = os.path.expanduser('~/StockDashboard/stock_dashboard_api')
load_dotenv(os.path.join(project_folder, '.env'))


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    RABBITMQ_CONNECTION_HOST = os.getenv('RABBITMQ_CONNECTION_HOST')
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')


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

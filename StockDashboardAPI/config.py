import os
from dotenv import load_dotenv
project_folder = os.path.expanduser('~/StockDashboard')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.venv'))


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '%#%@!#@#!@#!@#!@#!SJKDHA@KJ!H@K#JHJ'


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

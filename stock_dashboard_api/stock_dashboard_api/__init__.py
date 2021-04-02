import os

from flask import Flask

from stock_dashboard_api.stock_dashboard_api.config import DevelopmentConfig
from stock_dashboard_api.views import dashboard

TEMPLATE_FOLDER = os.path.join(os.environ.get('PROD_ROOT'), 'templates')

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)

app.config.from_object(DevelopmentConfig)

app.register_blueprint(dashboard.mod)

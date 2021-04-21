import json
import os

from flask import Flask

from stock_dashboard_api.config import DevelopmentConfig
from stock_dashboard_api.views import stock_view, dashboard_views, stocks_data_view, stock_config_view
import logging
from os import path

TEMPLATE_FOLDER = os.path.join(os.environ.get('PROD_ROOT'), 'templates')
app = Flask(__name__, template_folder=TEMPLATE_FOLDER)


log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path)

app.config.from_object(DevelopmentConfig)

app.register_blueprint(stock_view.mod)
app.register_blueprint(stocks_data_view.mod)
app.register_blueprint(dashboard_views.mod)
app.register_blueprint(stock_dashboard_view.mod)

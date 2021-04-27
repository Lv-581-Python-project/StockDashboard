import os

from flask import Flask

from stock_dashboard_api.config import DevelopmentConfig
from stock_dashboard_api.views import stock_view, mail_view, stocks_data_view, dashboard_view

TEMPLATE_FOLDER = os.path.join(os.environ.get('PROD_ROOT'), 'templates')
app = Flask(__name__, template_folder=TEMPLATE_FOLDER)

app.config.from_object(DevelopmentConfig)

app.register_blueprint(stock_view.mod)
app.register_blueprint(stocks_data_view.mod)
app.register_blueprint(mail_view.mod)
app.register_blueprint(dashboard_view.mod)

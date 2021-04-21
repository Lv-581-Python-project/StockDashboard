import os

from flask import Flask

from stock_dashboard_api.views import stock_view, dashboard_views, stocks_data_view, stock_dashboard_view

TEMPLATE_FOLDER = os.path.join(os.environ.get('PROD_ROOT'), 'templates')
app = Flask(__name__, template_folder=TEMPLATE_FOLDER)

app.config.from_object(os.environ.get('FLASK_DEVELOPMENT_CONFIG'))

app.register_blueprint(stock_view.mod)
app.register_blueprint(stocks_data_view.mod)
app.register_blueprint(dashboard_views.mod)
app.register_blueprint(stock_dashboard_view.mod)

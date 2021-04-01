from flask import Flask
from stock_dashboard_api.stock_dashboard_api.config import DevelopmentConfig
import os
from stock_dashboard_api.views import dashboard

# ROOT = os.environ.get('PROD_ROOT')
TEMPLATE_FOLDER = os.path.join('/home/slavko/Work/StockDashboard/stock_dashboard_api/templates')

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)

app.config.from_object(DevelopmentConfig)

app.register_blueprint(dashboard.mod)

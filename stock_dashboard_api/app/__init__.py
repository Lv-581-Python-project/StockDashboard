from flask import Flask
from .config import DevelopmentConfig

app = Flask(__name__, template_folder='/home/slavko/Work/StockDashboard/stock_dashboard_api/templates')

app.config.from_object(DevelopmentConfig)

from stock_dashboard_api import routes
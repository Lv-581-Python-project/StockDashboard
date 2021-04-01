from flask import Flask

from stock_dashboard_api.stock_dashboard_api.config import DevelopmentConfig

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)

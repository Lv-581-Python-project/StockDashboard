from flask import Flask

from stock_dashboard_api.config import DevelopmentConfig
from stock_dashboard_api.views.stock_view import stock_view_blueprint

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)
app.register_blueprint(stock_view_blueprint)

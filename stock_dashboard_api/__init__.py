from flask import Flask
from .config import DevelopmentConfig
from .views.stocks_data_view import stock_data_route
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

app.register_blueprint(stock_data_route)

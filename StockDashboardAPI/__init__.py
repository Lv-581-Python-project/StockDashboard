from flask import Flask
from StockDashboardAPI.config import DevelopmentConfig

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)


from StockDashboardAPI import routes

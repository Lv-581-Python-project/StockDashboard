import os

from flask import Flask
from flask_cors import CORS
from stock_dashboard_api.views import stock_view, mail_view, stocks_data_view, dashboard_view



TEMPLATE_FOLDER = os.path.join(os.environ.get('PROD_ROOT'), 'templates')
app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
cors = CORS(app)

app.config.from_object(os.environ.get('FLASK_CONFIG'))

app.register_blueprint(stock_view.mod)
app.register_blueprint(stocks_data_view.mod)
app.register_blueprint(mail_view.mod)
app.register_blueprint(dashboard_view.mod)

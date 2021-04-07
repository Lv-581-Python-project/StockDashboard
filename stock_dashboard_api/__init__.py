import json
import os
import re

from flask import Flask, request, make_response

from stock_dashboard_api.config import DevelopmentConfig
from stock_dashboard_api.views import stock_view, dashboard, stocks_data_view

TEMPLATE_FOLDER = os.path.join(os.environ.get('PROD_ROOT'), 'templates')
app = Flask(__name__, template_folder=TEMPLATE_FOLDER)

app.config.from_object(DevelopmentConfig)
app.register_blueprint(stock_view.mod)
app.register_blueprint(stocks_data_view.mod)
app.register_blueprint(dashboard.mod)


@app.before_request
def middleware_body_parse_json():
    if (request.method == 'PUT' and (
            re.match(r'/stocks_data/\d+', request.path) or re.match(r'/stocks/\d+', request.path))) or (
            request.method == 'POST' and (request.path == '/stocks_data/' or request.path == '/stocks/')):
        try:
            request.body = json.loads(request.get_json())
        except (ValueError, KeyError, TypeError):
            return make_response("Wrong data provided", 400)

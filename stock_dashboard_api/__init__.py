import json
import os

from flask import Flask, request, make_response

from stock_dashboard_api.config import DevelopmentConfig
from stock_dashboard_api.views import stock_view, dashboard_views, stocks_data_view, stock_config_view

TEMPLATE_FOLDER = os.path.join(os.environ.get('PROD_ROOT'), 'templates')
app = Flask(__name__, template_folder=TEMPLATE_FOLDER)

app.config.from_object(DevelopmentConfig)

app.register_blueprint(stock_view.mod)
app.register_blueprint(stocks_data_view.mod)
app.register_blueprint(dashboard_views.mod)
app.register_blueprint(stock_config_view.mod)

PATH_PATTERNS_BODY_PARSE_JSON = ['/stocks_data/', '/stocks/', '/stock_conf/']


@app.before_request
def middleware_body_parse_json():
    """A function that executes before request,
    receive and validate json data for PUT and POST request methods.
    """
    current_path = request.path
    if (request.method == 'PUT' and any(
            map(lambda pattern: current_path.startswith(pattern), PATH_PATTERNS_BODY_PARSE_JSON))) or (
            request.method == 'POST' and any(
            map(lambda pattern: current_path.startswith(pattern), PATH_PATTERNS_BODY_PARSE_JSON))):
        try:
            request.body = json.loads(request.data)
        except (ValueError, KeyError, TypeError):
            return make_response("Wrong data provided", 400)
import json
import os
import re

from flask import Flask, request, make_response

from stock_dashboard_api.config import DevelopmentConfig
from stock_dashboard_api.views import stock_view, dashboard_views, stocks_data_view

TEMPLATE_FOLDER = os.path.join(os.environ.get('PROD_ROOT'), 'templates')
app = Flask(__name__, template_folder=TEMPLATE_FOLDER)

app.config.from_object(DevelopmentConfig)
app.register_blueprint(stock_view.mod)
app.register_blueprint(stocks_data_view.mod)
app.register_blueprint(dashboard_views.mod)

PATH_PUT_PATTERNS = [r'/stocks_data/\d+', r'/stocks/\d+', r'/stock_conf/\d+']
PATH_POST_PATTERNS = ['/stocks_data/', '/stocks/', '/stock_conf/']
@app.before_request
def middleware_body_parse_json():  # pylint: disable=R1710
    current_path = request.path
    if (request.method == 'PUT' and any(map(lambda pattern:re.match(pattern,current_path), PATH_PUT_PATTERNS))) or (
            request.method == 'POST' and any(map(lambda pattern: current_path == pattern, PATH_POST_PATTERNS))):
        try:
            request.body = json.loads(request.get_json())
        except (ValueError, KeyError, TypeError):
            return make_response("Wrong data provided", 400)

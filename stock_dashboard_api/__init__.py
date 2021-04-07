import os
import json

from flask import Flask, request, make_response

from stock_dashboard_api.config import DevelopmentConfig
from stock_dashboard_api.views import stock_view, dashboard_views, stocks_data_view

TEMPLATE_FOLDER = os.path.join(os.environ.get('PROD_ROOT'), 'templates')
app = Flask(__name__, template_folder=TEMPLATE_FOLDER)

app.config.from_object(DevelopmentConfig)
app.register_blueprint(stock_view.mod)
app.register_blueprint(stocks_data_view.mod)
app.register_blueprint(dashboard_views.mod)


@app.before_request
def middleware_body_parse_json():
    if request.method == 'PUT' or request.method == 'POST':
        try:
            request.body = json.loads(request.get_json())
        except (ValueError, KeyError, TypeError):
            return make_response("Wrong data provided", 400)

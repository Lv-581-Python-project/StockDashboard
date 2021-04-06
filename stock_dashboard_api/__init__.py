import json

from flask import Flask, request, make_response

from stock_dashboard_api.config import DevelopmentConfig
from stock_dashboard_api.views import stocks_data_view

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)


@app.before_request
def middleware_body_parse_json():
    if request.method == 'PUT' or request.method == 'POST':
        try:
            request.body = json.loads(request.get_json())
        except (ValueError, KeyError, TypeError):
            return make_response("Wrong data provided", 400)


app.register_blueprint(stocks_data_view.mod)

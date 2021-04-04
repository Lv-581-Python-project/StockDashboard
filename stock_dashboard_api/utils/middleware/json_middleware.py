import json

from flask import request, make_response

from stock_dashboard_api.stock_dashboard_api import app


@app.before_request
def json_middleware():
    if request.method == 'PUT' or request.method == 'POST':
        try:
            request.body = json.loads(request.get_json())
        except (ValueError, KeyError, TypeError):
            return make_response("Wrong data provided", 400)

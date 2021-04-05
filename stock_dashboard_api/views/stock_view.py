import json

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from stock_dashboard_api.models.stock_model import Stock


class StockView(MethodView):
    def get(self, pk):
        if isinstance(pk, int):
            stock = Stock.get_by_id(pk)
            if stock:
                return make_response(jsonify(stock.to_dict()), 200)
        return make_response('Wrong data provided', 400)

    def post(self):
        try:
            body = request.get_json()
        except json.JSONDecodeError:
            return make_response("Wrong data provided", 400)
        stock_name, stock_company_name = body.get('name'), body.get('company_name')

        if isinstance(stock_name, str) and isinstance(stock_company_name, str) \
                and len(stock_name) <= 16 and len(stock_company_name) <= 128:
            stock_to_create = {'name': stock_name, 'company_name': stock_company_name}
        else:
            return make_response("Wrong data provided", 400)

        stock = Stock.create(**stock_to_create)
        if stock:
            return make_response(jsonify(stock.to_dict()), 200)
        return make_response("Failed to create Stock. Check input data", 400)

    def put(self, pk):
        stock = Stock.get_by_id(pk)
        if not stock:
            return make_response("Wrong data provided", 400)
        try:
            body = request.get_json()
        except json.JSONDecodeError:
            return make_response("Wrong data provided", 400)
        stock_name, stock_company_name = body.get('name'), body.get('company_name')
        stock_values_to_update = {}
        if isinstance(stock_name, str) and len(stock_name) <= 16:
            stock_values_to_update['name'] = stock_name
        if isinstance(stock_company_name, str) and len(stock_company_name) <= 128:
            stock_values_to_update['company_name'] = stock_company_name
        # MODEL HAVE TO RETURN NEW VALUE
        # IT IS POSSIBLE BY ADDING 'RETURNING' BLOCK TO SQL-QUERY, IN ORDER TO DO EVERYTHING AT ONCE
        # FIXME: it will fail, if model won't return new value
        if stock_values_to_update:
            stock = stock.update(**stock_values_to_update)
            if stock:
                return make_response(jsonify(stock.to_dict()), 200)
        return make_response("An error occurred during entity updating", 400)

    def delete(self, pk):
        if Stock.get_by_id(pk):
            # FIXME: add entity removal tracking
            Stock.delete_by_id(pk)
            return make_response('Removed successfully', 200)
        return make_response("Wrong data provided", 400)


stock_view_blueprint = Blueprint('stock', __name__, url_prefix='/stocks')

stock_view = StockView.as_view('stock_view')

stock_view_blueprint.add_url_rule('/', view_func=stock_view, methods=['POST', ])
stock_view_blueprint.add_url_rule('/<int:pk>', view_func=stock_view, methods=['GET', 'PUT', 'DELETE'])

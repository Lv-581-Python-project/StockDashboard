import json

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from stock_dashboard_api.models.stock_model import Stock

MAX_STOCK_NAME_LENGTH = 16
MAX_STOCK_COMPANY_NAME_LENGTH = 128


class StockView(MethodView):
    def get(self, pk):  # pylint: disable=C0103, R0201
        if isinstance(pk, int):
            stock = Stock.get_by_id(pk)
            if stock:
                return make_response(jsonify(stock.to_dict()), 200)
        return make_response('Wrong data provided', 400)

    def post(self):  # pylint: disable=R0201
        body = request.body
        stock_name, stock_company_name = body.get('name'), body.get('company_name')

        if isinstance(stock_name, str) \
                and isinstance(stock_company_name, str) \
                and len(stock_name) <= MAX_STOCK_NAME_LENGTH \
                and len(stock_company_name) <= MAX_STOCK_COMPANY_NAME_LENGTH:
            stock_to_create = {'name': stock_name, 'company_name': stock_company_name}
        else:
            return make_response("Wrong data provided", 400)

        stock = Stock.create(**stock_to_create)
        if stock:
            return make_response(jsonify(stock.to_dict()), 200)
        return make_response("Failed to create Stock. Check input data", 400)

    def put(self, pk):  # pylint: disable=C0103, R0201
        stock = Stock.get_by_id(pk)
        if not stock:
            return make_response("Wrong data provided", 400)
        body = request.body

        stock_name, stock_company_name = body.get('name'), body.get('company_name')
        stock_values_to_update = {}
        if isinstance(stock_name, str) and len(stock_name) <= MAX_STOCK_NAME_LENGTH:
            stock_values_to_update['name'] = stock_name
        if isinstance(stock_company_name, str) \
                and len(stock_company_name) <= MAX_STOCK_COMPANY_NAME_LENGTH:
            stock_values_to_update['company_name'] = stock_company_name
        if stock_values_to_update:
            stock = stock.update(**stock_values_to_update)
            if stock:
                return make_response(jsonify(stock.to_dict()), 200)
        return make_response("An error occurred during entity updating", 400)

    def delete(self, pk):  # pylint: disable=C0103, R0201
        if Stock.get_by_id(pk):
            if Stock.delete_by_id(pk):
                return make_response('Removed successfully', 200)
        return make_response("Wrong data provided", 400)


mod = Blueprint('stock', __name__, url_prefix='/stocks')

stock_view = StockView.as_view('stock_view')

mod.add_url_rule('/', view_func=stock_view, methods=['POST', ])
mod.add_url_rule('/<int:pk>', view_func=stock_view, methods=['GET', 'PUT', 'DELETE'])

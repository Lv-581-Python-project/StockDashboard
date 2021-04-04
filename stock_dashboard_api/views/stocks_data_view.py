import json

from flask import Blueprint, request, jsonify, make_response
from flask.views import MethodView

from stock_dashboard_api.models.stock_data_models import StocksData

mod = Blueprint('stocks_data', __name__, url_prefix='/stocks_data')


class StockDataView(MethodView):

    def get(self, pk):
        stock_data = StocksData.get_by_id(pk=pk)
        if stock_data is None:
            return make_response("Can not find stock data, wrong id", 400)
        return make_response(jsonify(stock_data.to_dict()), 200)

    def post(self):
        try:
            body = json.loads(request.get_json())

        except (ValueError, KeyError, TypeError):
            return make_response("Wrong data provided", 400)

        data_to_create = {
            'stock_id': body.get('stock_id'),
            'price': body.get('price'),
            'create_at': body.get('create_at')
        }
        stock_data = StocksData.create(**data_to_create)
        if stock_data is None:
            return make_response("Stock data is not created", 400)
        return make_response(jsonify(stock_data.to_dict()), 201)

    def put(self, pk):
        stock_data = StocksData.get_by_id(pk=pk)
        if stock_data is None:
            return make_response("Can not find stock data, wrong id", 400)

        try:
            body = json.loads(request.get_json())

        except (ValueError, KeyError, TypeError):
            return make_response("Wrong data provided", 400)

        data_to_update = {
            'price': body.get('price'),
            'create_at': body.get('create_at')
        }
        stock_data_updated = stock_data.update(**data_to_update)
        if stock_data_updated:
            return make_response(jsonify(stock_data_updated.to_dict()), 200)
        return make_response("Stock Data is not updated, possible you input wrong data", 400)

    def delete(self, pk):
        stock_data_deleted = StocksData.delete_by_id(pk=pk)
        if stock_data_deleted:
            return make_response("Stock data deleted", 200)
        return make_response("Stock data not deleted", 400)


stock_data_view = StockDataView.as_view('stock_data_view')
mod.add_url_rule('/', view_func=stock_data_view, methods=['POST', ])
mod.add_url_rule('/<int:pk>', view_func=stock_data_view, methods=['GET', 'PUT', 'DELETE'])

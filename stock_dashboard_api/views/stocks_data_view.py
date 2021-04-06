from datetime import datetime

from flask import Blueprint, request, jsonify, make_response
from flask.views import MethodView

from stock_dashboard_api.models.stock_data_models import StocksData

mod = Blueprint('stocks_data', __name__, url_prefix='/stocks_data')


class StockDataView(MethodView):

    def get(self, pk):  # pylint: disable=C0103, R0201
        stock_data = StocksData.get_by_id(pk=pk)
        if stock_data is None:
            return make_response("Can not find stock data, wrong id", 400)
        return make_response(jsonify(stock_data.to_dict()), 200)

    def post(self):  # pylint: disable=R0201
        price = request.body.get('price')
        create_at = request.body.get('create_at')
        stock_id = request.body.get('stock_id')
        if not isinstance(price, int):
            return make_response("Incorrect price specified, price should be integer (ex. 300)")
        if not isinstance(stock_id, int):
            return make_response("Incorrect stock id specified, stock id should be integer (ex. 1)")
        if not isinstance(create_at, str):
            return make_response(
                "Incorrect create_at specified, example '18/09/19 01:55:19'(year/month,day \
                hour:minute:second))", 400)
        try:
            create_at = datetime.strptime(create_at, '%y/%m/%d %H:%M:%S')
        except ValueError:
            return make_response(
                "Incorrect create_at specified, example '18/09/19 01:55:19'(year/month,day \
                hour:minute:second))", 400)
        data_to_create = {
            'price': price,
            'create_at': create_at,
            'stock_id': stock_id
        }
        stock_data = StocksData.create(**data_to_create)
        return make_response(jsonify(stock_data.to_dict()), 201)

    def put(self, pk):  # pylint: disable=C0103, R0201
        stock_data = StocksData.get_by_id(pk=pk)
        if stock_data is None:
            return make_response("Can not find stock data, wrong id", 400)
        price, create_at = request.body.get('price'), request.body.get('create_at')
        if not isinstance(price, int):
            return make_response("Incorrect price specified, \
            price should be integer (ex. 300)", 400)
        try:
            create_at = datetime.strptime(create_at, '%y/%m/%d %H:%M:%S')
        except ValueError:
            return make_response(
                "Incorrect date specified, example '18/09/19 01:55:19'(year/month,day \
                hour:minute:second))", 400)
        data_to_update = {
            'price': price,
            'create_at': create_at
        }
        stock_data_updated = stock_data.update(**data_to_update)
        if stock_data_updated:
            return make_response(jsonify(stock_data_updated.to_dict()), 200)
        return make_response("Stock Data is not updated, possible you input wrong data", 400)

    def delete(self, pk):  # pylint: disable=C0103, R0201
        stock_data_deleted = StocksData.delete_by_id(pk=pk)
        if stock_data_deleted:
            return make_response("Stock data deleted", 200)
        return make_response("Stock data not deleted", 400)


stock_data_view = StockDataView.as_view('stock_data_view')
mod.add_url_rule('/', view_func=stock_data_view, methods=['POST', ])
mod.add_url_rule('/<int:pk>', view_func=stock_data_view, methods=['GET', 'PUT', 'DELETE'])

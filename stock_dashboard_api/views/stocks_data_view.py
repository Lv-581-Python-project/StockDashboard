import json

from flask import Blueprint, Response, request
from flask.views import MethodView
from stock_dashboard_api.models.stock_data_models import StocksData

mod = Blueprint('stocks_data', __name__, url_prefix='/stocks_data')


class StockDataView(MethodView):

    def get(self, pk):
        stock_data = StocksData.get_by_id(pk=pk)
        if stock_data is None:
            return Response({"Error": "Can not find stock data, wrong id"}, status=400, mimetype='application/json')
        return Response({"id": stock_data.pk, "stock id": stock_data.stock_id,
                         "price": stock_data.price, "date": stock_data.date_time}, status=200,
                        mimetype='application/json')

    def post(self):
        try:
            body = request.get_json()
        except json.JSONDecodeError:
            return Response({"Error": "Invalid JSON"}, status=400, mimetype='application/json')

        data_to_create = {
            'stock_id': body.get('stock_id'),
            'price': body.get('price'),
            'date_time': body.get('date_time')
        }
        # TODO check if stock_id exists in Stock table
        stock_data = StocksData.create(**data_to_create)
        if stock_data is None:
            return Response({"Error": "Stock data is not created"}, status=400, mimetype='application/json')
        return Response(
            {"id": stock_data.pk, "stock id": stock_data.stock_id,
             "price": stock_data.price, "date": stock_data.date_time}, status=201,
            mimetype='application/json')

    def put(self, pk):
        stock_data = StocksData.get_by_id(pk=pk)
        if stock_data is None:
            return Response({"Error": "Can not find stock data, wrong id"}, status=400, mimetype='application/json')

        try:
            body = request.get_json()
        except json.JSONDecodeError:
            return Response({"Error": "Invalid JSON"}, status=400, mimetype='application/json')

        data_to_update = {
            'price': body.get('price'),
            'date_time': body.get('date_time')
        }
        stock_data_updated = stock_data.update(**data_to_update)
        # TODO check if stock_data is updated
        return Response({"id": stock_data_updated.pk, "stock id": stock_data_updated.stock_id,
                         "price": stock_data_updated.price, "date": stock_data_updated.date_time}, status=200,
                        mimetype='application/json')

    def delete(self, pk):
        stock_data_deleted = StocksData.delete_by_id(pk=pk)
        # TODO check if stock_data is deleted
        return Response({"Success": f"Stock data {pk} deleted"}, status=200, mimetype='application/json')


stock_data_view = StockDataView.as_view('stock_data_view')
mod.add_url_rule('/', view_func=stock_data_view, methods=['POST', ])
mod.add_url_rule('/<int:pk>', view_func=stock_data_view, methods=['GET', 'PUT', 'DELETE'])

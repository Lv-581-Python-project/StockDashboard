import json

from flask import Blueprint, Response, request
from flask.views import MethodView

from stock_dashboard_api.models.stock_data_models import StocksData

stock_data_route = Blueprint('stocks_data', __name__, url_prefix='/stocks_data')


class StockDataView(MethodView):

    def get(self, pk):
        if pk is None:
            return Response("{'Error':'Missing stock data id'}", status=404, mimetype='application/json')
        stock_data = StocksData.get_by_id(pk=pk)
        if stock_data is None:
            return Response({"Error": "Can not find stock data, wrong id"}, status=400, mimetype='application/json')
        return Response({"Stock data pk": stock_data.pk, "Stock data stock id": stock_data.stock_id,
                         "Stock data price": stock_data.price, "Stock data date": stock_data.date_time}, status=200,
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
            {"Created": "Success", "Stock data pk": stock_data.pk, "Stock data stock id": stock_data.stock_id,
             "Stock data price": stock_data.price, "Stock data date": stock_data.date_time}, status=201,
            mimetype='application/json')

    def put(self, pk):
        if pk is None:
            return Response("{'Error':'Missing stock data id'}", status=404, mimetype='application/json')
        stock_data = StocksData.get_by_id(pk=pk)
        if stock_data is None:
            return Response({"Error": "Can not find stock data, wrong id"}, status=400, mimetype='application/json')

        try:
            body = request.get_json()
        except json.JSONDecodeError:
            return Response({"Error": "Invalid JSON"}, status=400, mimetype='application/json')

        data_to_create = {
            'price': body.get('price'),
            'date_time': body.get('date_time')
        }
        stock_data_updated = stock_data.update(**data_to_create)
        # TODO check if stock_data is updated
        return Response({"Updated": "Success"}, status=200, mimetype='application/json')

    def delete(self, pk):
        stock_data_deleted = StocksData.delete_by_id(pk=pk)
        # TODO check if stock_data is deleted
        return Response({"Deleted": "Success"}, status=200, mimetype='application/json')


stock_data_view = StockDataView.as_view('stock_data_view')
stock_data_route.add_url_rule('/', view_func=stock_data_view, methods=['POST', ])
stock_data_route.add_url_rule('/<int:pk>', view_func=stock_data_view, methods=['GET', 'PUT', 'DELETE'])

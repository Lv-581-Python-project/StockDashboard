from datetime import datetime

from flask import Blueprint, request, jsonify, make_response, Response
from flask.views import MethodView

from stock_dashboard_api.models.stock_data_models import StockData

mod = Blueprint('stocks_data', __name__, url_prefix='/stocks_data')


class StockDataView(MethodView):
    """A StockDataView is a class-based view that inherits flask view - MethodView.
    This class implements get, put, post and delete methods to handle
    ``GET``, ``PUT``, ``POST``, ``DELETE`` requests accordingly.
    """

    def get(self, pk: int) -> Response:  # pylint: disable=C0103, R0201
        """A get method is used to send a specific GET request to access Stock Data by id

        :param pk: Stock Data primary key
        :return: a Response object with specific data and status code
        """
        stock_data = StockData.get_by_id(pk=pk)
        if stock_data is None:
            return make_response("Can not find stock data, wrong id", 400)
        return make_response(jsonify(stock_data.to_dict()), 200)

    def post(self) -> Response:  # pylint: disable=R0201
        """A post method is used to send a specific POST request to create Stock Data

        :return: a Response object with specific data and status code
        """
        price = request.body.get('price')
        create_at = request.body.get('create_at')
        stock_id = request.body.get('stock_id')
        if not isinstance(price, int):
            return make_response("Incorrect price specified, price should be integer (ex. 300)", 400)
        if not isinstance(stock_id, int):
            return make_response("Incorrect stock id specified, stock id should be integer (ex. 1)", 400)
        if not isinstance(create_at, str):
            return make_response(
                "Incorrect create_at specified, example '18/09/19 01:55:19'(year/month,day hour:minute:second))", 400)
        try:
            create_at = datetime.strptime(create_at, '%y/%m/%d %H:%M:%S')
        except ValueError:
            return make_response(
                "Incorrect create_at specified, example '18/09/19 01:55:19'(year/month,day hour:minute:second))", 400)
        data_to_create = {
            'price': price,
            'create_at': create_at,
            'stock_id': stock_id
        }
        stock_data = StockData.create(**data_to_create)
        return make_response(jsonify(stock_data.to_dict()), 201)

    def put(self, pk: int) -> Response:  # pylint: disable=C0103, R0201
        """A put method is used to send a specific PUT request to edit Stock Data by id

        :param pk: Stock Data primary key
        :return: a Response object with specific data and status code
        """
        stock_data = StockData.get_by_id(pk=pk)
        if stock_data is None:
            return make_response("Can not find stock data, wrong id", 400)
        price, create_at = request.body.get('price'), request.body.get('create_at')

        if price is not None and not isinstance(price, int):
            return make_response("Incorrect price specified, price should be integer (ex. 300)", 400)
        print(price)
        if create_at:
            if not isinstance(create_at, str):
                return make_response(
                    "Incorrect create_at specified, example '18/09/19 01:55:19'(year/month,day hour:minute:second))",
                    400)
            try:
                create_at = datetime.strptime(create_at, '%y/%m/%d %H:%M:%S')

            except ValueError:
                return make_response(
                    "Incorrect date specified, example '18/09/19 01:55:19'(year/month,day hour:minute:second))", 400)
        data_to_update = {
            "price": price,
            "create_at": create_at
        }
        stock_data_updated = stock_data.update(**data_to_update)
        if stock_data_updated:
            return make_response(jsonify(stock_data.to_dict()), 200)
        return make_response("Stock Data is not updated, possible you input wrong data", 400)

    def delete(self, pk: int) -> Response:  # pylint: disable=C0103, R0201
        """A delete method is used to send a specific DELETE request to delete Stock Data by id

        :param pk: Stock Data primary key
        :return: a Response object with specific data and status code
        """
        stock_data_deleted = StockData.delete_by_id(pk=pk)
        if stock_data_deleted:
            return make_response("Stock data deleted", 200)
        return make_response("Stock data not deleted", 400)


stock_data_view = StockDataView.as_view('stock_data_view')
mod.add_url_rule('/', view_func=stock_data_view, methods=['POST', ])
mod.add_url_rule('/<int:pk>', view_func=stock_data_view, methods=['GET', 'PUT', 'DELETE'])

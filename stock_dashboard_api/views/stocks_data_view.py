from datetime import datetime

from flask import Blueprint, request, jsonify, make_response, Response
from flask.views import MethodView
from stock_dashboard_api.utils.logger import views_logger as logger
from stock_dashboard_api.models.stock_data_models import StockData
from stock_dashboard_api.utils.json_parser import get_body
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
            message = "Can not find stock data, wrong id"
            logger.info(message)
            return make_response(message, 400)
        return make_response(jsonify(stock_data.to_dict()), 200)

    def post(self) -> Response:  # pylint: disable=R0201
        """A post method is used to send a specific POST request to create Stock Data

        :return: a Response object with specific data and status code
        """
        body = get_body(request)
        if not body:
            return make_response("Wrong data provided", 400)

        price = body.get('price')
        created_at = body.get('created_at')
        stock_id = body.get('stock_id')
        if not isinstance(price, int):
            message = "Incorrect price specified, price should be integer (ex. 300)"
            logger.info(message)
            return make_response(message, 400)
        if not isinstance(stock_id, int):
            message = "Incorrect stock id specified, stock id should be integer (ex. 1)"
            logger.info(message)
            return make_response(message, 400)
        if not isinstance(created_at, str):
            message = ("Incorrect created_at specified, "
                       "example '2018-09-19 01:55:19'(year-month-day hour:minute:second))")
            logger.info(message)
            return make_response(
                message, 400)

        try:
            created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
        except ValueError:

            message = ("Incorrect created_at specified, "
                       "example '2018-09-19 01:55:19'(year-month-day hour:minute:second))")
            logger.info(message)
            return make_response(
                message, 400)

        data_to_create = {
            'price': price,
            'created_at': created_at,
            'stock_id': stock_id
        }
        stock_data = StockData.create(**data_to_create)
        if stock_data:
            return make_response(jsonify(stock_data.to_dict()), 201)
        return make_response("Creating error", 400)

    def put(self, pk: int) -> Response:  # pylint: disable=C0103, R0201
        """A put method is used to send a specific PUT request to edit Stock Data by id

        :param pk: Stock Data primary key
        :return: a Response object with specific data and status code
        """
        body = get_body(request)
        if not body:
            return make_response("Wrong data provided", 400)
        stock_data = StockData.get_by_id(pk=pk)
        if stock_data is None:
            message = "Can not find stock data, wrong id"
            logger.info(message)
            return make_response(message, 400)
        price, created_at = body.get('price'), body.get('created_at')

        if price is not None and not isinstance(price, int):
            message = "Incorrect price specified, price should be integer (ex. 300)"
            logger.info(message)
            return make_response(message, 400)

        if created_at:
            if not isinstance(created_at, str):
                message = ("Incorrect created_at specified, "
                           "example '2018-09-19 01:55:19'(year-month-day hour:minute:second)")
                logger.info(message)
                return make_response(message, 400)
            try:
                created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                message = "Incorrect date specified, example '2018-09-19 01:55:19'(year-month-day hour:minute:second))"
                logger.info(message)
                return make_response(message, 400)

        data_to_update = {
            "price": price,
            "created_at": created_at
        }
        stock_data_updated = stock_data.update(**data_to_update)

        if stock_data_updated:
            return make_response(jsonify(stock_data.to_dict()), 200)
        message = "Stock Data is not updated, possible you input wrong data"
        logger.info(message)
        return make_response(message, 400)

    def delete(self, pk: int) -> Response:  # pylint: disable=C0103, R0201
        """A delete method is used to send a specific DELETE request to delete Stock Data by id

        :param pk: Stock Data primary key
        :return: a Response object with specific data and status code
        """
        stock_data_deleted = StockData.delete_by_id(pk=pk)
        if stock_data_deleted:
            return make_response("Stock data deleted", 200)
        message = "Stock data not deleted"
        logger.info(message)
        return make_response(message, 400)


stock_data_view = StockDataView.as_view('stock_data_view')
mod.add_url_rule('/<int:pk>', view_func=stock_data_view, methods=['GET'])

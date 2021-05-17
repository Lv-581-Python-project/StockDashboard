import json
from datetime import datetime

from flask import Blueprint, request, make_response, jsonify, Response
from flask.views import MethodView

from stock_dashboard_api.models.stock_model import Stock
from stock_dashboard_api.utils.constants import DATETIME_PATTERN
from stock_dashboard_api.utils.json_parser import get_body
from stock_dashboard_api.utils.logger import views_logger as logger
from stock_dashboard_api.utils.scheduler_queue import publish_task
from stock_dashboard_api.utils.yahoo_finance import check_if_exist, get_meta_data

MAX_STOCK_NAME_LENGTH = 16
MAX_STOCK_COMPANY_NAME_LENGTH = 128
QUEUE = "new_stocks_data_download_queue"


class StockView(MethodView):
    """
    A StockView is a class-based view that inherits flask view - MethodView.
    This class implements get, put, post and delete methods to handle
    ``GET``, ``PUT``, ``POST``, ``DELETE`` requests accordingly.
    """

    def get(self, pk: int = None) -> Response:  # pylint: disable=C0103, R0201
        """A method that return all Stocks, or Stock if provided pk is valid, or if provided valid pk 'from' and 'to'
         in query string, this method return list of stock data for some period of time.

        :param pk: Stock primary key (id)
        :return: Response with all Stocks or one Stock if provided valid pk, or list of stock data for some period of
         time if provided valid pk, from, to
        """
        body = get_body(request)
        if pk:
            return self._get_by_id(pk)
        if body is None:
            return self._get_all()
        else:
            name = body["validate_stock"]["name"]
            if check_if_exist(name):
                queue_body = json.dumps({"queue": QUEUE, "name": name})
                publish_task(queue_body)
                data = get_meta_data(name)
                stock = Stock.create(data["name"], data["company_name"], data["country"], data["industry"], data["sector"])
                return make_response(jsonify(stock.to_dict()), 200)
            message = "A non-existent stock is entered."
            return make_response(message, 400)

    def post(self) -> Response:  # pylint: disable=R0201
        """A method that create Stock and return it if provided data is valid

        :return: Response with just created Stock
        """
        body = get_body(request)
        stock_name, stock_company_name = body.get('name'), body.get('company_name')

        if isinstance(stock_name, str) \
                and isinstance(stock_company_name, str) \
                and len(stock_name) <= MAX_STOCK_NAME_LENGTH \
                and len(stock_company_name) <= MAX_STOCK_COMPANY_NAME_LENGTH:
            stock_to_create = {'name': stock_name, 'company_name': stock_company_name}
        else:
            message = "Wrong data provided"
            logger.info(message)
            return make_response(message, 400)

        stock = Stock.create(**stock_to_create)
        if stock:
            return make_response(jsonify(stock.to_dict()), 200)
        message = "Failed to create Stock. Check input data"
        logger.info(message)
        return make_response(message, 400)

    def put(self, pk: int) -> Response:  # pylint: disable=C0103, R0201
        """A method that update Stock if provided data is valid

        :param pk: Stock primary key (id)
        :return: Response with just updated Stock
        """
        body = get_body(request)
        stock = Stock.get_by_id(pk)
        if not stock:
            message = "Wrong data provided"
            logger.info(message)
            return make_response(message, 400)

        stock_name, stock_company_name = body.get('name'), body.get('company_name')
        stock_values_to_update = {}
        if isinstance(stock_name, str) and len(stock_name) <= MAX_STOCK_NAME_LENGTH:
            stock_values_to_update['name'] = stock_name
        if isinstance(stock_company_name, str) \
                and len(stock_company_name) <= MAX_STOCK_COMPANY_NAME_LENGTH:
            stock_values_to_update['company_name'] = stock_company_name
        if stock_values_to_update:
            stock.update(**stock_values_to_update)
            if stock:
                return make_response(jsonify(stock.to_dict()), 200)
        message = "An error occurred during entity updating"
        logger.info(message)
        return make_response(message, 400)

    def delete(self, pk: int) -> Response:  # pylint: disable=C0103, R0201
        """A method that remove Stock if provided pk is valid

        :param pk: Stock primary key (id)
        :return: Response with result message
        """
        if Stock.delete_by_id(pk):
            return make_response('Removed successfully', 200)
        message = "Wrong data provided"
        logger.info(message)
        return make_response(message, 400)

    def _get_all(self):
        """
        A method that return all Stocks
        :return: Response with all Stocks
        """
        stocks = [stock.to_dict() for stock in Stock.get_all()]
        return make_response(jsonify(stocks), 200)

    def _get_by_id(self, pk: int):  # pylint: disable=C0103, R0201
        """A method that return Stock if provided pk is valid, or if provided valid pk 'from' and 'to'
        in query string, this method return list of stock data for some period of time.

        :param pk: Stock primary key (id)
        :return: Response with one Stock
        """
        stock = Stock.get_by_id(pk)
        if not stock:
            message = 'Wrong data provided'
            logger.info(message)
            return make_response(message, 400)
        datetime_from, datetime_to = request.args.get('from'), request.args.get('to')
        if datetime_from and datetime_to:
            return self._get_data_for_time_period(stock=stock, datetime_from=datetime_from, datetime_to=datetime_to)
        return make_response(jsonify(stock.to_dict()), 200)

    def _get_data_for_time_period(self, stock: Stock, datetime_from: str, datetime_to: str):
        try:
            datetime_from = datetime.strptime(datetime_from, DATETIME_PATTERN)
            datetime_to = datetime.strptime(datetime_to, DATETIME_PATTERN)
        except ValueError:
            return make_response(
                "Incorrect date specified, example '2018-09-19 01:55:19'(year-month-day hour:minute:second)",
                400)
        stock_data_for_time_period = stock.get_data_for_time_period(datetime_from, datetime_to)
        stock_data_for_time_period = [stock_data.to_dict() for stock_data in stock_data_for_time_period]
        return make_response(jsonify(stock_data_for_time_period), 200)


mod = Blueprint('stock', __name__, url_prefix='/api/stocks')

stock_view = StockView.as_view('stock_view')

mod.add_url_rule('/', view_func=stock_view, methods=['GET', 'POST'])
mod.add_url_rule('/<int:pk>', view_func=stock_view, methods=['GET', 'PUT', 'DELETE'])

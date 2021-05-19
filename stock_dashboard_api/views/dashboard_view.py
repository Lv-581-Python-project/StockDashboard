from flask.views import MethodView
from flask import Blueprint, request, jsonify, make_response, Response
from stock_dashboard_api.utils.logger import views_logger as logger
from stock_dashboard_api.models.dashboard_model import Dashboard
from stock_dashboard_api.models.stock_model import Stock
from stock_dashboard_api.utils.json_parser import get_body
mod = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


class DashboardView(MethodView):
    """A DashboardView is a class-based view that inherits flask view - MethodView.
    This class implements get and post methods to handle
    ``GET``, ``POST`` requests accordingly.
    """

    def get(self, dashboard_hash: str) -> Response:
        """A get method is used to send a specific GET request to access Dashboard by config_hash

        :param dashboard_hash: Dashboard unique field
        :return: a Response object with specific data and status code
        """
        dashboard = Dashboard.get_by_hash(dashboard_hash=dashboard_hash)
        if dashboard is None:
            message = "Can not find dashboard, wrong hash"
            logger.info(message)
            return make_response(message, 400)
        stocks = dashboard.get_stocks()
        if not stocks:
            return make_response("Can not find any stocks in dashboard", 400)
        stocks = [stock.to_dict() for stock in stocks]
        return make_response(jsonify({"stocks": stocks}), 200)

    def post(self) -> Response:
        """A post method is used to send a specific POST request to create Dashboard

        :return: a Response object with specific data and status code
        """
        body = get_body(request)
        if not body:
            return make_response("Wrong data provided", 400)
        stock_ids = body.get('all_stocks')
        if not stock_ids:
            return make_response("No stock ids provided", 400)
        stock_ids = [stock["id"] for stock in stock_ids]
        stocks = Stock.get_stock_by_ids(stock_ids)
        if not stocks:
            return make_response("Wrong stock ids provided", 400)
        dashboard = Dashboard.create(stocks=stocks)
        if dashboard:
            return make_response(jsonify(dashboard.to_dict()), 201)
        return make_response("Can not create a dashboard", 400)

    def delete(self, dashboard_hash):
        stock_config_deleted = Dashboard.delete_by_hash(dashboard_hash=dashboard_hash)
        if stock_config_deleted:
            return make_response("Stock config deleted successfully", 200)
        message = "Stock config not deleted"
        logger.info(message)
        return make_response(message, 400)

    def put(self, dashboard_hash):
        stock_config = Dashboard.get_by_hash(dashboard_hash=dashboard_hash)
        config_hash = str(request.body.get('config_hash'))
        if stock_config is None:
            message = "Cannot find stock config data, wrong id"
            logger.info(message)
            return make_response(message, 400)

        stock_config_updated = stock_config.update(config_hash)
        if stock_config_updated:
            return make_response(jsonify(stock_config.to_dict()), 200)
        message = "Stock Config wasn't updated, check your input data"
        logger.info(message)
        return make_response(message, 400)


class DashboardStocksView(MethodView):
    def get(self) -> Response:
        stock_ids = request.args.get('stock_ids')
        if not stock_ids[1:-1]:
            return make_response('Wrong data provided', 400)
        stocks = []
        for stock_pk in stock_ids[1:-1].split(", "):
            taken_stock = Stock.get_by_id(stock_pk)
            if not taken_stock:
                return make_response(f"Can not find stock, wrong id", 400)
            stocks.append([stock.to_dict() for stock in Stock.get_data_for_last_day(int(stock_pk))])
        return make_response(jsonify(stocks), 200)


dashboard_view = DashboardView.as_view('dashboard')
mod.add_url_rule('/<string:dashboard_hash>', view_func=dashboard_view, methods=['GET'])
mod.add_url_rule('/', view_func=dashboard_view, methods=['POST'])
stock_dashboard_stocks_view = DashboardStocksView.as_view('stock_dashboard_stocks_view')
mod.add_url_rule('/', view_func=stock_dashboard_stocks_view, methods=['GET', ])

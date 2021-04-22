from flask.views import MethodView
from flask import Blueprint, request, jsonify, make_response, Response
from stock_dashboard_api.utils.logger import views_logger as logger
from stock_dashboard_api.models.dashboard_model import Dashboard
from stock_dashboard_api.utils.json_parser import get_body

mod = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


class DashboardView(MethodView):
    """A DashboardView is a class-based view that inherits flask view - MethodView.
    This class implements get and post methods to handle
    ``GET``, ``POST`` requests accordingly.
    """

    def get(self, config_hash: str) -> Response:
        """A get method is used to send a specific GET request to access Dashboard by config_hash

        :param config_hash: Dashboard unique field
        :return: a Response object with specific data and status code
        """
        dashboard = Dashboard.get_by_hash(config_hash=config_hash)
        if dashboard is None:
            message = "Can not find dashboard, wrong hash"
            logger.info(message)
            return make_response(message, 400)
        stocks = dashboard.get_stocks()
        print(stocks)
        if not stocks:
            return make_response("Can not find any stocks in dashboard", 400)
        return make_response(jsonify({"stocks": stocks}), 200)

    def post(self) -> Response:
        """A post method is used to send a specific POST request to create Dashboard

        :return: a Response object with specific data and status code
        """
        body = get_body(request)
        if not body:
            return make_response("Wrong data provided", 400)
        stocks = body.get('stocks')
        dashboard = Dashboard.create(stocks=stocks)
        if dashboard:
            return make_response(jsonify(dashboard.to_dict()), 201)
        return make_response("Can not create a dashboard", 400)


dashboard_view = DashboardView.as_view('dashboard')
mod.add_url_rule('/<string:config_hash>', view_func=dashboard_view, methods=['GET'])
mod.add_url_rule('/', view_func=dashboard_view, methods=['POST'])

from flask.views import MethodView
from flask import Blueprint, request, jsonify, make_response, Response
from stock_dashboard_api.utils.logger import views_logger as logger
from stock_dashboard_api.models.dashboard_model import Dashboard
from stock_dashboard_api.utils.json_parser import middleware_body_parse_json
from stock_dashboard_api.utils.config_hash_generator import generate_uuid

mod = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


class DashboardView(MethodView):

    def get(self, config_hash: str) -> Response:
        dashboard = Dashboard.get_by_hash(config_hash=config_hash)
        if dashboard is None:
            message = "Can not find dashboard, wrong hash"
            logger.info(message)
            return make_response(message, 400)
        stocks = dashboard.get_stocks_by_dashboard_id()
        if stocks is None:
            return make_response("Can not find any stocks in dashboard", 400)
        return make_response(jsonify({"stocks": stocks}), 200)

    def post(self):
        response = middleware_body_parse_json(request)
        if not response:
            return make_response("Wrong data provided", 400)
        stocks = request.body.get('stocks')
        config_hash = generate_uuid()
        dashboard = Dashboard.create(config_hash=config_hash, stocks=stocks)
        if dashboard:
            return make_response(jsonify(dashboard.to_dict()), 201)
        return make_response("Can not create a dashboard", 400)


dashboard_view = DashboardView.as_view('dashboard')
mod.add_url_rule('/<string:config_hash>', view_func=dashboard_view, methods=['GET'])
mod.add_url_rule('/', view_func=dashboard_view, methods=['POST'])

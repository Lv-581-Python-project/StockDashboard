from flask import Blueprint, request, jsonify, make_response, Response
from flask.views import MethodView

from stock_dashboard_api.utils.logger import views_logger as logger
from stock_dashboard_api.models.dashboard_model import Dashboard

mod = Blueprint('stock_conf', __name__, url_prefix='/stock_conf')


class StockDashboardView(MethodView):

    def get(self, pk: int) -> Response:  # pylint: disable=C0103, R0201
        stock_config = Dashboard.get_by_id(pk=pk)
        if stock_config is None:
            message = "Can not find stock config, wrong id"
            logger.info(message)
            return make_response(message, 400)
        return make_response(jsonify(stock_config.to_dict()), 200)

    def delete(self, pk):  # pylint: disable=C0103, R0201
        stock_config_deleted = Dashboard.delete_by_id(pk=pk)
        if stock_config_deleted:
            return make_response("Stock config deleted successfully", 200)
        message = "Stock config not deleted"
        logger.info(message)
        return make_response(message, 400)

    def post(self):  # pylint: disable=R0201
        config_hash = str(request.body.get('config_hash'))
        if not config_hash:
            message = "Please provide hash for config creation"
            logger.info(message)
            return make_response(message, 400)
        stock_config = Dashboard.create(config_hash=config_hash)
        if not stock_config:
            message = "Please make sure that hash has correct length and format"
            logger.info(message)
            return make_response(message, 400)
        return make_response(jsonify(stock_config.to_dict()), 201)

    def put(self, pk):  # pylint: disable=C0103, R0201
        stock_config = Dashboard.get_by_id(pk=pk)
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


stock_config_view = StockDashboardView.as_view('stock_config_view')
mod.add_url_rule('/', view_func=stock_config_view, methods=['POST', ])
mod.add_url_rule('/<int:pk>', view_func=stock_config_view, methods=['GET', 'PUT', 'DELETE'])

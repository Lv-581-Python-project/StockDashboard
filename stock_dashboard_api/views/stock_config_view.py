from flask import Blueprint, request, jsonify, make_response
from flask.views import MethodView

from stock_dashboard_api.models.dashboard_config_models import DashboardConfig

mod = Blueprint('stock_conf', __name__, url_prefix='/stock_conf')


class StockConfigView(MethodView):

    def get(self, pk):  # pylint: disable=C0103, R0201
        stock_config = DashboardConfig.get_by_id(pk=pk)
        if stock_config is None:
            return make_response("Can not find stock config, wrong id", 400)
        return make_response(jsonify(stock_config.to_dict()), 200)

    def delete(self, pk):  # pylint: disable=C0103, R0201
        stock_config_deleted = DashboardConfig.delete_by_id(pk=pk)
        if stock_config_deleted:
            return make_response("Stock config deleted successfully", 200)
        return make_response("Stock config not deleted", 400)

    def post(self):  # pylint: disable=R0201
        config_hash = str(request.body.get('config_hash'))
        if not config_hash:
            return make_response(
                "Please provide hash for config creation", 400)
        stock_config = DashboardConfig.create(config_hash=config_hash)
        return make_response(jsonify(stock_config.to_dict()), 201)

    def put(self, pk):  # pylint: disable=C0103, R0201
        stock_config = DashboardConfig.get_by_id(pk=pk)
        config_hash = str(request.body.get('config_hash'))
        if stock_config is None:
            return make_response("Cannot find stock config data, wrong id", 400)

        stock_config_updated = stock_config.update(config_hash)
        if stock_config_updated:
            return make_response(jsonify(stock_config_updated.to_dict()), 200)
        return make_response("Stock Config wasn't updated, check your input data", 400)


stock_config_view = StockConfigView.as_view('stock_config_view')
mod.add_url_rule('/', view_func=stock_config_view, methods=['POST', ])
mod.add_url_rule('/<int:pk>', view_func=stock_config_view, methods=['GET', 'PUT', 'DELETE'])
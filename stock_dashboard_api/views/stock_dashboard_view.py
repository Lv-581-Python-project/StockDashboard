from flask import Blueprint, request, jsonify, make_response, Response
from flask.views import MethodView

from stock_dashboard_api.models.dashboard_model import Dashboard
from stock_dashboard_api.models.stock_model import Stock

mod = Blueprint('stock_conf', __name__, url_prefix='/api/dashboard')


class StockDashboardView(MethodView):

    def get(self, pk: int) -> Response:  # pylint: disable=C0103, R0201
        stock_config = Dashboard.get_by_id(pk=pk)
        if stock_config is None:
            return make_response("Can not find stock config, wrong id", 400)
        return make_response(jsonify(stock_config.to_dict()), 200)

    def delete(self, pk):  # pylint: disable=C0103, R0201
        stock_config_deleted = Dashboard.delete_by_id(pk=pk)
        if stock_config_deleted:
            return make_response("Stock config deleted successfully", 200)
        return make_response("Stock config not deleted", 400)

    def post(self):  # pylint: disable=R0201
        config_hash = str(request.body.get('config_hash'))
        if not config_hash:
            return make_response("Please provide hash for config creation", 400)
        stock_config = Dashboard.create(config_hash=config_hash)
        if not stock_config:
            return make_response("Please make sure that hash has correct length and format", 400)
        return make_response(jsonify(stock_config.to_dict()), 201)

    def put(self, pk):  # pylint: disable=C0103, R0201
        stock_config = Dashboard.get_by_id(pk=pk)
        config_hash = str(request.body.get('config_hash'))
        if stock_config is None:
            return make_response("Cannot find stock config data, wrong id", 400)

        stock_config_updated = stock_config.update(config_hash)
        if stock_config_updated:
            return make_response(jsonify(stock_config.to_dict()), 200)
        return make_response("Stock Config wasn't updated, check your input data", 400)


class StockDashboardStocksView(MethodView):
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


stock_config_view = StockDashboardView.as_view('stock_config_view')
stock_dashboard_stocks_view = StockDashboardStocksView.as_view('stock_dashboard_stocks_view')
mod.add_url_rule('/', view_func=stock_config_view, methods=['POST', ])
mod.add_url_rule('/<int:pk>', view_func=stock_config_view, methods=['GET', 'PUT', 'DELETE'])
mod.add_url_rule('/', view_func=stock_dashboard_stocks_view, methods=['GET', ])

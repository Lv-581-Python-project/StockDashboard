from flask.views import MethodView
from flask import Blueprint, Response

view_route = Blueprint('stocks_data', __name__, url_prefix='/stocks_data')


class StocksDataView(MethodView):

    def get(self, pk):
        if pk is None:
            return Response("{'Error':'Missing stock data id'}", status=404, mimetype='application/json')

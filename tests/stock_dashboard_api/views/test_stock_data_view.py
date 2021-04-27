import json
import os

from unittest.mock import patch

from flask import Blueprint
from stock_dashboard_api import app
from stock_dashboard_api.models.stock_data_models import StockData
from stock_dashboard_api.views import stocks_data_view

# Flask app configuration for testing
test_mod = Blueprint('test_stocks_data', stocks_data_view.__name__, url_prefix='/stocks_data')
app.config.from_object(os.environ.get('FLASK_TESTING_CONFIG'))
test_mod.add_url_rule('/', view_func=stocks_data_view.stock_data_view, methods=['POST', ])
test_mod.add_url_rule('/<int:pk>', view_func=stocks_data_view.stock_data_view, methods=['PUT', 'DELETE'])
app.register_blueprint(test_mod)


@patch('stock_dashboard_api.models.stock_data_models.StockData.get_by_id')
def test_get_pass(mock_get):
    with app.app_context():
        mock_get.return_value = StockData(stock_id=2, price=300, created_at="18-09-19 01:55:19", pk=1)
        with app.test_client() as client:
            response = client.get('/stocks_data/1')
            body = json.loads(response.data)
            assert response.status_code == 200
            assert body['id'] == 1
            assert body['created_at'] == '18-09-19 01:55:19'
            assert body['price'] == 300
            assert body['stock_id'] == 2


@patch('stock_dashboard_api.models.stock_data_models.StockData.get_by_id')
def test_get_fail(mock_get):
    with app.app_context():
        message = b"Can not find stock data, wrong id"
        mock_get.return_value = None
        with app.test_client() as client:
            response = client.get('/stocks_data/2')
            assert response.status_code == 400
            assert response.data == message


@patch('stock_dashboard_api.models.stock_data_models.StockData.create')
def test_post_pass(mock_post):
    with app.app_context():
        mock_post.return_value = StockData(stock_id=1, price=500, created_at="2020-05-11 04:22:30")
        with app.test_client() as client:
            data = {
                "price": 500,
                "created_at": "2020-05-11 04:22:30",
                "stock_id": 1
            }
            response = client.post('/stocks_data/', json=data)
            assert response.status_code == 201
            body = json.loads(response.data)
            assert response.status_code == 201
            assert body['created_at'] == "2020-05-11 04:22:30"
            assert body['price'] == 500
            assert body['stock_id'] == 1


def test_post_data_fail():
    with app.test_client() as client:
        message = b"Wrong data provided"
        incorrect_json = '{ "stock_id:"12 "price":30 "created_at:"None" }'
        response = client.post('/stocks_data/', data=incorrect_json)
        assert response.status_code == 400
        assert response.data == message
        response = client.post('/stocks_data/')
        assert response.status_code == 400
        assert response.data == message


def test_post_data_fail_wrong_price():
    with app.test_client() as client:
        message = b"Incorrect price specified, price should be integer (ex. 300)"
        data = {"stock_id": 3,
                "price": "wrong",
                "created_at": "18/09/19 01:55:19"}
        response = client.post('/stocks_data/', json=data)
        assert response.status_code == 400
        assert response.data == message


def test_post_data_fail_wrong_stock_id():
    with app.test_client() as client:
        message = b"Incorrect stock id specified, stock id should be integer (ex. 1)"
        data = {"stock_id": "wrong",
                "price": 300,
                "createв_at": "18/09/19 01:55:19"}
        response = client.post('/stocks_data/', json=data)
        assert response.status_code == 400
        assert response.data == message


def test_post_data_fail_wrong_create_at():
    with app.test_client() as client:
        message = b"Incorrect created_at specified, example '2018-09-19 01:55:19'(year-month-day hour:minute:second))"
        data = {"stock_id": 3,
                "price": 300,
                "created_at": "20-01-01"}
        response = client.post('/stocks_data/', json=data)
        assert response.status_code == 400
        assert response.data == message


@patch('stock_dashboard_api.models.stock_data_models.StockData.create')
def test_post_create_fail(mock_post):
    with app.app_context():
        message = b"Incorrect created_at specified, example '2018-09-19 01:55:19'(year-month-day hour:minute:second))"
        mock_post.return_value = None
        with app.test_client() as client:
            data = {"stock_id": 3,
                    "price": 300
                    }
            response = client.post('/stocks_data/', json=data)
            assert response.status_code == 400
            assert response.data == message


@patch('stock_dashboard_api.models.stock_data_models.StockData.get_by_id')
@patch('stock_dashboard_api.models.stock_data_models.StockData.update')
def test_put_success(mock_get, mock_put):
    with app.app_context():
        mock_get.return_value = StockData(stock_id=2, price=300, created_at="2020-08-19 01:55:19", pk=1)
        mock_put.return_value = StockData(stock_id=2, price=500, created_at="2020-09-19 01:55:19", pk=1)
        with app.test_client() as client:
            data = {"price": 500,
                    "created_at": "2020-09-19 01:55:19"
                    }
            response = client.put('/stocks_data/1', json=data)
            body = json.loads(response.data)
            assert response.status_code == 200
            assert body['created_at'] == "2020-09-19 01:55:19"
            assert body['price'] == 500
            assert body['stock_id'] == 2


@patch('stock_dashboard_api.models.stock_data_models.StockData.get_by_id')
def test_put_not_existing_pk(mock_get):
    with app.app_context():
        message = b"Can not find stock data, wrong id"
        mock_get.return_value = None
        with app.test_client() as client:
            data = {"price": 500,
                    "created_at": "2021-01-08"
                    }
            response = client.put('/stocks_data/2', json=data)
            assert response.status_code == 400
            assert response.data == message


@patch('stock_dashboard_api.models.stock_data_models.StockData.get_by_id')
def test_put_wrong_json(mock_get):
    with app.app_context():
        message = b"Wrong data provided"
        mock_get.return_value = StockData(stock_id=2, price=300, created_at="2020-09-19 01:55:19", pk=1)
        with app.test_client() as client:
            incorrect_json = '{ "stock_id:"12 "price":30 "created_at:"None" }'
            response = client.put('/stocks_data/2', data=incorrect_json)
            assert response.status_code == 400
            assert response.data == message


@patch('stock_dashboard_api.models.stock_data_models.StockData.get_by_id')
def test_put_wrong_price(mock_get):
    with app.app_context():
        message = b"Incorrect price specified, price should be integer (ex. 300)"
        mock_get.return_value = StockData(stock_id=2, price=300, created_at="19/09/19 01:55:19", pk=1)
        with app.test_client() as client:
            data = {"price": "wrong",
                    "created_at": "19/09/19 01:55:19"
                    }
            response = client.put('/stocks_data/2', json=data)
            assert response.status_code == 400
            assert response.data == message


@patch('stock_dashboard_api.models.stock_data_models.StockData.get_by_id')
def test_put_wrong_create_at(mock_get):
    with app.app_context():
        message = b"Incorrect date specified, example '2018-09-19 01:55:19'(year-month-day hour:minute:second))"
        mock_get.return_value = StockData(stock_id=2, price=300, created_at="19/09/19 01:55:19", pk=1)
        with app.test_client() as client:
            data = {"price": 300,
                    "created_at": "2021/01/08"
                    }
            response = client.put('/stocks_data/2', json=data)
            assert response.status_code == 400
            assert response.data == message


@patch('stock_dashboard_api.models.stock_data_models.StockData.get_by_id')
@patch('stock_dashboard_api.models.stock_data_models.StockData.update')
def test_put_unknown_error(mock_put, mock_get):
    with app.app_context():
        message = b"Stock Data is not updated, possible you input wrong data"
        mock_get.return_value = StockData(stock_id=2, price=300, created_at="18/09/19 01:55:19", pk=1)
        mock_put.return_value = None
        with app.test_client() as client:
            data = {"price": 500,
                    "created_at": "2020-09-19 01:55:19"
                    }
            response = client.put('/stocks_data/1', json=data)
            assert response.status_code == 400
            assert response.data == message


@patch('stock_dashboard_api.models.stock_data_models.StockData.delete_by_id')
def test_delete_success(mock_delete):
    with app.app_context():
        message = b"Stock data deleted"
        mock_delete.return_value = True
        with app.test_client() as client:
            response = client.delete('/stocks_data/1')
            assert response.status_code == 200
            assert response.data == message


@patch('stock_dashboard_api.models.stock_data_models.StockData.delete_by_id')
def test_delete_fail(mock_delete):
    with app.app_context():
        message = b"Stock data not deleted"
        mock_delete.return_value = None
        with app.test_client() as client:
            response = client.delete('/stocks_data/1')
            assert response.status_code == 400
            assert response.data == message

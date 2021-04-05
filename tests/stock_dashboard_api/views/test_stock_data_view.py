import json
from unittest.mock import patch

from stock_dashboard_api.models.stock_data_models import StocksData
from stock_dashboard_api import app


@patch('stock_dashboard_api.models.stock_data_models.StocksData.get_by_id')
def test_get_pass(mock_get):
    with app.app_context():
        mock_get.return_value = StocksData(stock_id=2, price=300, create_at="2021-01-01", pk=1)
        with app.test_client() as client:
            response = client.get('/stocks_data/1')
            body = json.loads(response.data)
            assert response.status_code == 200
            assert body['id'] == 1
            assert body['create_at'] == '2021-01-01'
            assert body['price'] == 300
            assert body['stock_id'] == 2


@patch('stock_dashboard_api.models.stock_data_models.StocksData.get_by_id')
def test_get_fail(mock_get):
    with app.app_context():
        mock_get.return_value = None
        with app.test_client() as client:
            response = client.get('/stocks_data/2')
            assert response.status_code == 400
            assert response.data == b"Can not find stock data, wrong id"


@patch('stock_dashboard_api.models.stock_data_models.StocksData.create')
def test_post_pass(mock_post):
    with app.app_context():
        mock_post.return_value = StocksData(stock_id=3, price=300, create_at="2020-01-01")
        with app.test_client() as client:
            data = json.dumps({"stock_id": 3,
                               "price": 300,
                               "create_at": "2020-01-01"})
            response = client.post('/stocks_data/', json=data)
            body = json.loads(response.data)
            assert response.status_code == 201
            assert body['create_at'] == '2020-01-01'
            assert body['price'] == 300
            assert body['stock_id'] == 3


def test_post_data_fail():
    with app.test_client() as client:
        incorrect_json = '{ "stock_id:"12 "price":30 "create_at:"None" }'
        response = client.post('/stocks_data/', json=incorrect_json)
        assert response.status_code == 400
        assert response.data == b"Wrong data provided"
        response = client.post('/stocks_data/')

        assert response.status_code == 400
        assert response.data == b"Wrong data provided"


@patch('stock_dashboard_api.models.stock_data_models.StocksData.create')
def test_post_create_fail(mock_post):
    with app.app_context():
        mock_post.return_value = None
        with app.test_client() as client:
            data = json.dumps({"stock_id": 3,
                               "price": 300
                               })
            response = client.post('/stocks_data/', json=data)
            assert response.status_code == 400
            assert response.data == b"Stock data is not created"


@patch('stock_dashboard_api.models.stock_data_models.StocksData.get_by_id')
@patch('stock_dashboard_api.models.stock_data_models.StocksData.update')
def test_put_success(mock_put, mock_get):
    with app.app_context():
        mock_get.return_value = StocksData(stock_id=2, price=300, create_at="2021-01-01", pk=1)
        mock_put.return_value = StocksData(stock_id=2, price=500, create_at="2021-01-08", pk=1)
        with app.test_client() as client:
            data = json.dumps({"price": 500,
                               "create_at": "2021-01-08"
                               })
            response = client.put('/stocks_data/1', json=data)
            body = json.loads(response.data)
            assert response.status_code == 200
            assert body['id'] == 1
            assert body['create_at'] == '2021-01-08'
            assert body['price'] == 500
            assert body['stock_id'] == 2


@patch('stock_dashboard_api.models.stock_data_models.StocksData.get_by_id')
def test_put_not_existing_pk(mock_get):
    with app.app_context():
        mock_get.return_value = None
        with app.test_client() as client:
            data = json.dumps({"price": 500,
                               "create_at": "2021-01-08"
                               })
            response = client.put('/stocks_data/2', json=data)
            assert response.status_code == 400
            assert response.data == b"Can not find stock data, wrong id"


@patch('stock_dashboard_api.models.stock_data_models.StocksData.get_by_id')
def test_put_wrong_json(mock_get):
    with app.app_context():
        mock_get.return_value = StocksData(stock_id=2, price=300, create_at="2021-01-01", pk=1)
        with app.test_client() as client:
            incorrect_json = '{ "stock_id:"12 "price":30 "create_at:"None" }'
            response = client.put('/stocks_data/2', json=incorrect_json)
            assert response.status_code == 400
            assert response.data == b"Wrong data provided"


@patch('stock_dashboard_api.models.stock_data_models.StocksData.get_by_id')
@patch('stock_dashboard_api.models.stock_data_models.StocksData.update')
def test_put_wrong_values(mock_put, mock_get):
    with app.app_context():
        mock_get.return_value = StocksData(stock_id=2, price=300, create_at="2021-01-01", pk=1)
        mock_put.return_value = None
        with app.test_client() as client:
            data = json.dumps({"price": "ajif",
                               "create_at": "2021-01-08"
                               })
            response = client.put('/stocks_data/2', json=data)
            assert response.status_code == 400
            assert response.data == b"Stock Data is not updated, possible you input wrong data"


@patch('stock_dashboard_api.models.stock_data_models.StocksData.delete_by_id')
def test_delete_success(mock_delete):
    with app.app_context():
        mock_delete.return_value = True
        with app.test_client() as client:
            response = client.delete('/stocks_data/1')
            assert response.status_code == 200
            assert response.data == b"Stock data deleted"


@patch('stock_dashboard_api.models.stock_data_models.StocksData.delete_by_id')
def test_delete_fail(mock_delete):
    with app.app_context():
        mock_delete.return_value = None
        with app.test_client() as client:
            response = client.delete('/stocks_data/1')
            assert response.status_code == 400
            assert response.data == b"Stock data not deleted"

import json

from unittest.mock import patch
from stock_dashboard_api import app
from stock_dashboard_api.models.dashboard_model import Dashboard


@patch('stock_dashboard_api.models.dashboard_model.Dashboard.get_stocks')
@patch('stock_dashboard_api.models.dashboard_model.Dashboard.get_by_hash')
def test_get_dashboard_pass(mock_get, mock_get_stocks):
    with app.app_context():
        mock_get.return_value = Dashboard(pk=1, config_hash='awf241af')
        mock_get_stocks.return_value = [1, 2]
        with app.test_client() as client:
            response = client.get('/api/dashboard/awf241af')
            body = json.loads(response.data)
            assert response.status_code == 200
            assert body['stocks'] == [1, 2]


@patch('stock_dashboard_api.models.dashboard_model.Dashboard.get_by_hash')
def test_get_dashboard_wrong_hash(mock_get):
    message = b'Can not find dashboard, wrong hash'
    with app.app_context():
        mock_get.return_value = None
        with app.test_client() as client:
            response = client.get('/api/dashboard/bbf03b8')
            assert response.status_code == 400
            assert response.data == message


@patch('stock_dashboard_api.models.dashboard_model.Dashboard.get_stocks')
@patch('stock_dashboard_api.models.dashboard_model.Dashboard.get_by_hash')
def test_get_dashboard_fail_no_stocks(mock_get, mock_get_stocks):
    message = b'Can not find any stocks in dashboard'
    with app.app_context():
        mock_get.return_value = Dashboard(pk=1, config_hash='00e947a3')
        mock_get_stocks.return_value = []
        with app.test_client() as client:
            response = client.get('/api/dashboard/00e947a3')
            assert response.status_code == 400
            assert response.data == message


@patch('stock_dashboard_api.models.dashboard_model.Dashboard.create')
def test_post_dashboard_pass(mock_post):
    data = {"stocks": [{"stock_id": 1, "datetime_from": "2018-09-19 01:55:19", "datetime_to": "2018-09-25 01:55:19"},
                       {"stock_id": 2, "datetime_from": "2018-09-19 01:55:19", "datetime_to": "2018-09-25 01:55:19"}]}
    with app.app_context():
        mock_post.return_value = Dashboard(pk=1, config_hash='00e947a3')
        with app.test_client() as client:
            response = client.post('/api/dashboard/', json=data)
            body = json.loads(response.data)
            assert response.status_code == 201
            assert body["pk"] == 1
            assert body["config_hash"] == "00e947a3"


def test_post_dashboard_fail_invalid_data():
    message = b"Wrong data provided"
    incorrect_json = '{ "stocks: [1,23,4]" }'
    with app.test_client() as client:
        response = client.post('/api/dashboard/', data=incorrect_json)
        assert response.status_code == 400
        assert response.data == message


@patch('stock_dashboard_api.models.dashboard_model.Dashboard.create')
def test_post_dashboard_fail_invalid_date(mock_post):
    message = b"Can not create a dashboard"
    data = {"stocks": [{"stock_id": 1, "datetime_from": "18-09-19 01:55:19", "datetime_to": "2018-09-25 01:55:19"},
                       {"stock_id": 2, "datetime_from": "18-09-19 01:55:19", "datetime_to": "2018-09-25 01:55:19"}]}

    with app.app_context():
        mock_post.return_value = None
        with app.test_client() as client:
            response = client.post('/api/dashboard/', json=data)
            assert response.status_code == 400
            assert response.data == message

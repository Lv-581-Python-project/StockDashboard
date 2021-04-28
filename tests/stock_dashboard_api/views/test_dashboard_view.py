import json

from unittest.mock import patch
from stock_dashboard_api import app
from stock_dashboard_api.models.dashboard_model import Dashboard
from stock_dashboard_api.models.stock_model import Stock


@patch('stock_dashboard_api.models.dashboard_model.Dashboard.get_stocks')
@patch('stock_dashboard_api.models.dashboard_model.Dashboard.get_by_hash')
def test_get_dashboard_pass(mock_get, mock_get_stocks):
    with app.app_context():
        mock_get.return_value = Dashboard(dashboard_hash='awf241af')
        mock_get_stocks.return_value = [
            Stock(pk=1, name="A", company_name="Agilent Technologies Inc. Common Stock", in_use=False)]
        with app.test_client() as client:
            response = client.get('/api/dashboard/awf241af')
            body = json.loads(response.data)
            assert response.status_code == 200
            assert body['stocks'] == [
                {
                    "company_name": "Agilent Technologies Inc. Common Stock",
                    "id": 1,
                    "in_use": False,
                    "name": "A"
                }]


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
        mock_get.return_value = Dashboard(dashboard_hash='00e947a3')
        mock_get_stocks.return_value = []
        with app.test_client() as client:
            response = client.get('/api/dashboard/00e947a3')
            assert response.status_code == 400
            assert response.data == message


@patch('stock_dashboard_api.models.dashboard_model.Dashboard.create')
def test_post_dashboard_pass(mock_post):
    data = {"stocks": [
        {
            "company_name": "Agilent Technologies Inc. Common Stock",
            "id": 1,
            "in_use": False,
            "name": "A"
        },
        {
            "company_name": "Alcoa Corporation Common Stock ",
            "id": 2,
            "in_use": False,
            "name": "AA"
        },
        {
            "company_name": "Ares Acquisition Corporation Class A Ordinary Shares",
            "id": 3,
            "in_use": False,
            "name": "AAC"
        }
    ]}
    with app.app_context():
        mock_post.return_value = Dashboard(dashboard_hash='00e947a3')
        with app.test_client() as client:
            response = client.post('/api/dashboard/', json={"stock_ids": [1, 2, 3]})
            assert response.status_code == 201



def test_post_dashboard_fail_invalid_data():
    message = b"Wrong data provided"
    incorrect_json = '{ "stocks: [1,23,4]" }'
    with app.test_client() as client:
        response = client.post('/api/dashboard/', data=incorrect_json)
        assert response.status_code == 400
        assert response.data == message

import json
from unittest import TestCase
from unittest.mock import patch

from stock_dashboard_api import app
from stock_dashboard_api.models.dashboard_model import Dashboard
from stock_dashboard_api.models.stock_model import Stock


class DashboardViewsTestCase(TestCase):
    @patch('stock_dashboard_api.models.dashboard_model.Dashboard.get_stocks')
    @patch('stock_dashboard_api.models.dashboard_model.Dashboard.get_by_hash')
    def test_get_dashboard_pass(self, mock_get, mock_get_stocks):
        with app.app_context():
            mock_get.return_value = Dashboard(dashboard_hash='awf241af')
            mock_get_stocks.return_value = [
                Stock(pk=1,
                      name="A",
                      company_name="Agilent Technologies Inc. Common Stock",
                      country="United States",
                      industry="Biotechnology: Laboratory Analytical Instruments",
                      sector="Capital Goods",
                      in_use=False)]
            with app.test_client() as client:
                response = client.get('/api/dashboard/awf241af')
                body = json.loads(response.data)
                assert response.status_code == 200
                assert body['stocks'] == [
                    {
                        "company_name": "Agilent Technologies Inc. Common Stock",
                        "id": 1,
                        "in_use": False,
                        "name": "A",
                        "country": "United States",
                        "industry": "Biotechnology: Laboratory Analytical Instruments",
                        "sector": "Capital Goods"
                    }]

    @patch('stock_dashboard_api.models.dashboard_model.Dashboard.get_by_hash')
    def test_get_dashboard_wrong_hash(self, mock_get):
        message = b'Can not find dashboard, wrong hash'
        with app.app_context():
            mock_get.return_value = None
            with app.test_client() as client:
                response = client.get('/api/dashboard/bbf03b8')
                assert response.status_code == 400
                assert response.data == message

    @patch('stock_dashboard_api.models.dashboard_model.Dashboard.get_stocks')
    @patch('stock_dashboard_api.models.dashboard_model.Dashboard.get_by_hash')
    def test_get_dashboard_fail_no_stocks(self, mock_get, mock_get_stocks):
        message = b'Can not find any stocks in dashboard'
        with app.app_context():
            mock_get.return_value = Dashboard(dashboard_hash='00e947a3')
            mock_get_stocks.return_value = []
            with app.test_client() as client:
                response = client.get('/api/dashboard/00e947a3')
                assert response.status_code == 400
                assert response.data == message

    @patch('stock_dashboard_api.models.dashboard_model.Dashboard.create')
    @patch('stock_dashboard_api.models.stock_model.Stock.get_stock_by_ids')
    @patch('stock_dashboard_api.models.stock_model.Stock.get_by_id')
    def test_post_dashboard_pass(self, mock_get_by_id, mock_get_ids, mock_post):
        data = {"all_stocks": [{"id": 1, "name": "A"}], "missing_names": []}
        with app.app_context():
            mock_get_ids.return_value = Stock(pk=1,
                                              name="A",
                                              company_name="Agilent Technologies Inc. Common Stock",
                                              country="United States",
                                              industry="Biotechnology: Laboratory Analytical Instruments",
                                              sector="Capital Goods",
                                              in_use=False)
            mock_post.return_value = Dashboard(dashboard_hash='f79ee4f2')
            mock_get_by_id.return_value = Stock(pk=1,
                                                name="A",
                                                company_name="Agilent Technologies Inc. Common Stock",
                                                country="United States",
                                                industry="Biotechnology: Laboratory Analytical Instruments",
                                                sector="Capital Goods",
                                                in_use=True)
            with app.test_client() as client:
                response = client.post('/api/dashboard/', json=data)
                assert response.status_code == 201

    def test_post_dashboard_fail_invalid_data(self):
        message = b"Wrong data provided"
        incorrect_json = '{ "stocks: [1,23,4]" }'
        with app.test_client() as client:
            response = client.post('/api/dashboard/', data=incorrect_json)
            assert response.status_code == 400
            assert response.data == message

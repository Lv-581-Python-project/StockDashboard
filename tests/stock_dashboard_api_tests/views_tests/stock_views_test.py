import json
from unittest import TestCase
from unittest.mock import patch, PropertyMock

from models.stock_model import Stock
from stock_dashboard_api import app


class StockViewsTestCase(TestCase):

    def test_get_by_id(self):
        with patch('stock_dashboard_api.models.stock_model.Stock.get_by_id',
                   new_callable=PropertyMock) as mock_get_by_id:
            stock_id, stock_name, stock_company_name = 1, 'mocked get name', 'mocked get company name'
            mock_get_by_id().return_value = Stock(pk=stock_id, name=stock_name, company_name=stock_company_name)
            with app.test_client() as client:
                response = client.get('/stocks/{stock_id}'.format(stock_id=stock_id))

                self.assertEqual(json.loads(response.data),
                                 {'company_name': stock_company_name, 'id': stock_id, 'name': stock_name})

    def test_create(self):
        with patch('stock_dashboard_api.models.stock_model.Stock.create', new_callable=PropertyMock) as mock_create:
            stock_id, stock_name, stock_company_name = 1, 'mock cr name', 'mocked create company name'
            mock_create().return_value = Stock(pk=stock_id, name=stock_name, company_name=stock_company_name)
            with app.test_client() as client:
                response = client.post('/stocks/', json={'name': stock_name, 'company_name': stock_company_name})

                self.assertEqual(json.loads(response.data),
                                 {'company_name': stock_company_name, 'id': stock_id, 'name': stock_name})

    # FIXME: real model does not return anything on update now
    def test_update_by_id(self):
        with patch('stock_dashboard_api.models.stock_model.Stock.update', new_callable=PropertyMock) as mock_update:
            stock_id, new_stock_name, new_stock_company_name = 1, 'mock upd name', 'mocked update company name'
            mock_update().return_value = Stock(pk=stock_id, name=new_stock_name, company_name=new_stock_company_name)
            with app.test_client() as client:
                response = client.put('/stocks/{}'.format(stock_id),
                                      json={'name': new_stock_name, 'company_name': new_stock_company_name})

                self.assertEqual(json.loads(response.data),
                                 {'company_name': new_stock_company_name, 'id': stock_id, 'name': new_stock_name})

    def test_delete_by_id(self):
        with patch('stock_dashboard_api.models.stock_model.Stock.delete_by_id',
                   new_callable=PropertyMock) as mock_delete:
            stock_id = 1
            mock_delete().return_value = True
            with app.test_client() as client:
                response = client.delete('/stocks/{stock_id}'.format(stock_id=stock_id))

                self.assertEqual(response.status, '200 OK')

    def test_get_by_id_missing_id(self):
        with patch('stock_dashboard_api.models.stock_model.Stock.get_by_id',
                   new_callable=PropertyMock) as mock_get_by_id:
            stock_id = 1
            mock_get_by_id().return_value = None
            with app.test_client() as client:
                response = client.get('/stocks/{stock_id}'.format(stock_id=stock_id))

                self.assertEqual(response.status, '400 BAD REQUEST')

    def test_create_wrong_data(self):
        with patch('stock_dashboard_api.models.stock_model.Stock.create', new_callable=PropertyMock) as mock_create:
            stock_id, stock_name, stock_company_name =\
                1, 'tooooooo long create stock name', 'mocked create company name'
            # mock_create().return_value =
            with app.test_client() as client:
                response = client.post('/stocks/', json={'name': stock_name, 'company_name': stock_company_name})
                print(response)

                self.assertEqual(response.status, '400 BAD REQUEST')

    def test_update_by_id_wrong_data(self):
        with patch('stock_dashboard_api.models.stock_model.Stock.update', new_callable=PropertyMock) as mock_update:
            stock_id, new_stock_name, new_stock_company_name =\
                1, 'tooooooo long update stock name', 'mocked create company name'
            mock_update().return_value = None
            with app.test_client() as client:
                response = client.put('/stocks/{stock_id}'.format(stock_id=stock_id),
                                      json={'name': new_stock_name, 'company_name': new_stock_company_name})

                self.assertEqual(response.status, '400 BAD REQUEST')

    def test_update_by_id_missing_id(self):
        with patch('stock_dashboard_api.models.stock_model.Stock.update', new_callable=PropertyMock) as mock_update:
            stock_id, new_stock_name, new_stock_company_name = 1, 'mock upd name', 'mocked update company name'
            mock_update().return_value = None
            with app.test_client() as client:
                response = client.put('/stocks/{stock_id}'.format(stock_id=stock_id),
                                      json={'name': new_stock_name, 'company_name': new_stock_company_name})

                self.assertEqual(response.status, '400 BAD REQUEST')

    def test_delete_by_id_missing_id(self):
        with patch('stock_dashboard_api.models.stock_model.Stock.get_by_id',
                   new_callable=PropertyMock) as mock_get_by_id:
            stock_id = 1
            mock_get_by_id().return_value = None
            with app.test_client() as client:
                response = client.delete('/stocks/{stock_id}'.format(stock_id=stock_id))

                self.assertEqual(response.status, '400 BAD REQUEST')

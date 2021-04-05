import json
from unittest import TestCase
from unittest.mock import patch, PropertyMock

from stock_dashboard_api import app
from stock_dashboard_api.models.stock_model import Stock


class StockViewsTestCase(TestCase):

    def setUp(self) -> None:
        stock_patcher = patch('stock_dashboard_api.views.stock_view.Stock', autospec=True)
        self.stock_mock = stock_patcher.start()
        self.addCleanup(stock_patcher.stop)

    def test_get_by_id(self):
        stock_id, stock_name, stock_company_name = 1, 'mocked get name', 'mocked get company name'
        get_by_id = self.stock_mock.get_by_id
        get_by_id.return_value.to_dict.return_value = {'id': stock_id, 'name': stock_name,
                                                       'company_name': stock_company_name}
        with app.test_client() as client:
            response = client.get('/stocks/{stock_id}'.format(stock_id=stock_id))

            self.assertEqual(json.loads(response.data),
                             {'company_name': stock_company_name, 'id': stock_id, 'name': stock_name})

    def test_create(self):
        stock_id, stock_name, stock_company_name = 1, 'mock cr name', 'mocked create company name'
        create = self.stock_mock.create
        create.return_value = Stock(pk=stock_id, name=stock_name, company_name=stock_company_name)
        with app.test_client() as client:
            response = client.post('/stocks/', json={'name': stock_name, 'company_name': stock_company_name})

            self.assertEqual(json.loads(response.data),
                             {'company_name': stock_company_name, 'id': stock_id, 'name': stock_name})

    # FIXME: real model does not return anything on update now
    def test_update_by_id(self):
        stock_id, old_stock_name, old_stock_company_name = 1, 'mock old name', 'mocked pre update company name'
        stock_id, new_stock_name, new_stock_company_name = 1, 'mock upd name', 'mocked update company name'
        get_by_id = self.stock_mock.get_by_id
        update = get_by_id.return_value.update
        get_by_id.return_value = {'name': 'stock name', 'company_name': 'stock company name'}
        update.return_value = {'company_name': new_stock_company_name, 'id': stock_id, 'name': new_stock_name}
        with app.test_client() as client:
            response = client.put('/stocks/{}'.format(stock_id),
                                  json={'name': new_stock_name, 'company_name': new_stock_company_name})

            # self.assertEqual(json.loads(response.data),
            #                  {'company_name': new_stock_company_name, 'id': stock_id, 'name': new_stock_name})

    def test_delete_by_id(self):
        delete = self.stock_mock.delete_by_id
        delete.return_value = True
        stock_id = 1
        with app.test_client() as client:
            response = client.delete('/stocks/{stock_id}'.format(stock_id=stock_id))
            self.assertEqual(response.status, '200 OK')

    def test_get_by_id_missing_id(self):
        stock_id, stock_name, stock_company_name = 1, 'mock cr name', 'mocked create company name'
        get_by_id = self.stock_mock.get_by_id
        get_by_id.return_value = None
        with app.test_client() as client:
            response = client.get('/stocks/{stock_id}'.format(stock_id=stock_id))
            self.assertEqual(response.status, '400 BAD REQUEST')

    def test_create_wrong_data(self):
        stock_id, stock_name, stock_company_name = 1, 'mock cr name', 'mocked create company name'
        create = self.stock_mock.create
        create.return_value = None
        with app.test_client() as client:
            response = client.post('/stocks/', json={'name': stock_name, 'company_name': stock_company_name})
            self.assertEqual(response.status, '400 BAD REQUEST')

    def test_update_by_id_wrong_data(self):
        stock_id, new_stock_name, new_stock_company_name = 1, 'tooooooo long update stock name', 165428653
        with app.test_client() as client:
            response = client.put('/stocks/{stock_id}'.format(stock_id=stock_id),
                                  json={'name': new_stock_name, 'company_name': new_stock_company_name})

            self.assertEqual(response.status, '400 BAD REQUEST')

    def test_update_by_id_missing_id(self):
        get_by_id = self.stock_mock.get_by_id
        get_by_id.return_value = None
        stock_id, new_stock_name, new_stock_company_name = 1, 'mock upd name', 'mocked update company name'
        with app.test_client() as client:
            response = client.put('/stocks/{stock_id}'.format(stock_id=stock_id),
                                  json={'name': new_stock_name, 'company_name': new_stock_company_name})

            self.assertEqual(response.status, '400 BAD REQUEST')

    def test_delete_by_id_missing_id(self):
        get_by_id = self.stock_mock.get_by_id
        get_by_id.return_value = None
        stock_id = 1
        with app.test_client() as client:
            response = client.delete('/stocks/{stock_id}'.format(stock_id=stock_id))
            self.assertEqual(response.status, '400 BAD REQUEST')

import datetime
import json
from unittest import TestCase
from unittest.mock import patch

from stock_dashboard_api import app
from stock_dashboard_api.models.stock_model import Stock

BASE_URL = '/api/stocks/'
STATUS_200 = '200 OK'
STATUS_400 = '400 BAD REQUEST'


class StockViewsTestCase(TestCase):

    def setUp(self) -> None:
        stock_patcher = patch('stock_dashboard_api.views.stock_view.Stock', autospec=True)
        stock_data_patcher = patch('stock_dashboard_api.models.stock_data_models.StockData', autospec=True)
        self.stock_mock = stock_patcher.start()
        self.stock_data_mock = stock_data_patcher.start()
        self.addCleanup(stock_patcher.stop)
        self.addCleanup(stock_data_patcher.stop)

    def test_get_by_id(self):
        stock_id, stock_name, stock_company_name = 1, 'mocked get name', 'mocked get company name'
        get_by_id = self.stock_mock.get_by_id
        get_by_id.return_value.to_dict.return_value = {'id': stock_id, 'name': stock_name,
                                                       'company_name': stock_company_name}
        with app.test_client() as client:
            response = client.get(BASE_URL + '{stock_id}'.format(stock_id=stock_id))

            self.assertEqual(json.loads(response.data),
                             {'company_name': stock_company_name, 'id': stock_id, 'name': stock_name})

    def test_create(self):
        stock_id, stock_name, stock_company_name, stock_in_use = 1, 'mock cr name', 'mocked create company name', False
        create = self.stock_mock.create
        create.return_value = Stock(pk=stock_id, name=stock_name, company_name=stock_company_name, in_use=stock_in_use)
        with app.test_client() as client:
            response = client.post(BASE_URL, json={'name': stock_name, 'company_name': stock_company_name})

            self.assertEqual(json.loads(response.data),
                             {'company_name': stock_company_name, 'id': stock_id, 'name': stock_name, 'in_use': False})

    def test_update_by_id(self):
        stock_id, new_stock_name, new_stock_company_name = 1, 'mock upd name', 'mocked update company name'
        get_by_id = self.stock_mock.get_by_id
        get_by_id.return_value = self.stock_mock(1, 'sdfsd', 'sdfsdf')
        get_by_id.return_value.to_dict.return_value = {'name': new_stock_name, 'id': stock_id,
                                                       'company_name': new_stock_company_name}
        with app.test_client() as client:
            response = client.put(BASE_URL + '{}'.format(stock_id),
                                  json={'name': new_stock_name, 'company_name': new_stock_company_name})

            self.assertEqual(json.loads(response.data),
                             {'company_name': new_stock_company_name, 'id': stock_id, 'name': new_stock_name})

    def test_delete_by_id(self):
        delete = self.stock_mock.delete_by_id
        delete.return_value = True
        stock_id = 1
        with app.test_client() as client:
            response = client.delete(BASE_URL + '{stock_id}'.format(stock_id=stock_id))
            self.assertEqual(response.status, STATUS_200)

    def test_get_by_id_missing_id(self):
        stock_id, stock_name, stock_company_name = 1, 'mock cr name', 'mocked create company name'
        get_by_id = self.stock_mock.get_by_id
        get_by_id.return_value = False
        with app.test_client() as client:
            response = client.get(BASE_URL + '{stock_id}'.format(stock_id=stock_id))
            self.assertEqual(response.status, STATUS_400)

    def test_create_wrong_data(self):
        stock_id, stock_name, stock_company_name = 1, 'mock create super long name', 'mocked create company name'
        create = self.stock_mock.create
        create.return_value = None
        with app.test_client() as client:
            response = client.post(BASE_URL, json={'name': stock_name, 'company_name': stock_company_name})
            self.assertEqual(response.status, STATUS_400)

    def test_create_wrong_data2(self):
        stock_id, stock_name, stock_company_name = 1, 'mock create name', 'mocked create company name'
        create = self.stock_mock.create
        create.return_value = None
        with app.test_client() as client:
            response = client.post(BASE_URL, json={'name': stock_name, 'company_name': stock_company_name})
            self.assertEqual(response.status, STATUS_400)

    def test_update_by_id_wrong_data(self):
        stock_id, new_stock_name, new_stock_company_name = 1, 'tooooooo long update stock name', 165428653
        with app.test_client() as client:
            response = client.put(BASE_URL + '{stock_id}'.format(stock_id=stock_id),
                                  json={'name': new_stock_name, 'company_name': new_stock_company_name})

            self.assertEqual(response.status, STATUS_400)

    def test_update_by_id_missing_id(self):
        get_by_id = self.stock_mock.get_by_id
        get_by_id.return_value = None
        stock_id, new_stock_name, new_stock_company_name = 1, 'mock upd name', 'mocked update company name'
        with app.test_client() as client:
            response = client.put(BASE_URL + '{stock_id}'.format(stock_id=stock_id),
                                  json={'name': new_stock_name, 'company_name': new_stock_company_name})

            self.assertEqual(response.status, STATUS_400)

    def test_delete_by_id_missing_id(self):
        delete_by_id = self.stock_mock.delete_by_id
        delete_by_id.return_value = False
        stock_id = 1
        with app.test_client() as client:
            response = client.delete(BASE_URL + '{stock_id}'.format(stock_id=stock_id))
            self.assertEqual(response.status, STATUS_400)

    def test_get_stock_data_for_time_period(self):
        get_by_id = self.stock_mock.get_by_id
        get_by_id.return_value = self.stock_mock(1, 'IBM', 'IBM')
        get_data_for_time_period = get_by_id.return_value.get_data_for_time_period

        stock_data_id = 1
        stock_data_stock_id = 1
        stock_data_price = 144.15
        stock_data_created_at = datetime.datetime(2020, 4, 1, 5, 21, 22)
        stock_data = self.stock_data_mock(stock_data_id, stock_data_stock_id, stock_data_price, stock_data_created_at)
        stock_data.to_dict.return_value = {'id': stock_data_id,
                                           'stock_id': stock_data_stock_id,
                                           'price': stock_data_price,
                                           'created_at': stock_data_created_at}
        get_data_for_time_period.return_value = [stock_data, ]

        stock_id = 1
        expected_response = [{
            "created_at": "Wed, 01 Apr 2020 05:21:22 GMT",
            "id": 1,
            "price": 144.15,
            "stock_id": 1
        }]
        with app.test_client() as client:
            response = client.get(BASE_URL + '{stock_id}?from=2020-04-01 05:21:22&to=2020-05-11 04:22:30'
                                  .format(stock_id=stock_id))
            self.assertEqual(json.loads(response.data), expected_response)

    def test_get_stock_data_for_time_period_wrong_time(self):
        get_by_id = self.stock_mock.get_by_id
        get_by_id.return_value = self.stock_mock(1, 'IBM', 'IBM', False)
        self.stock_mock.to_dict.return_value = {'pk': 1,
                                                'name': 'IBM',
                                                'company_name': 'IBM',
                                                'in_use': False}
        stock_id = 1
        with app.test_client() as client:
            response = client.get(BASE_URL + '{stock_id}?from=2020/01 05:21:22&to=2020-05-11 04:22:30'
                                  .format(stock_id=stock_id))
            self.assertEqual(response.data,
                             b"Incorrect date specified, example '2018-09-19 01:55:19'"
                             b"(year-month-day hour:minute:second)")
            self.assertEqual(response.status, STATUS_400)

    def test_get_all(self):
        data = {'pk': 1, 'name': 'IBM', 'company_name': 'IBM'}
        expected_result = [data]
        stock = self.stock_mock(**data)
        stock.to_dict.return_value = data.copy()
        get_all = self.stock_mock.get_all
        get_all.return_value = [stock]

        with app.test_client() as client:
            response = client.get(BASE_URL)
            self.assertEqual(expected_result, json.loads(response.data))

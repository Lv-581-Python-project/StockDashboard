import unittest
from unittest.mock import patch

import psycopg2

from stock_dashboard_api.models import stock_model as sm


@patch('stock_dashboard_api.models.stock_model.pool_manager')
class TestStock(unittest.TestCase):

    def test_create_true(self, pool_manager):
        data = {"id": 1, "name": "AAPL", "company_name": "Apple"}
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (1, "AAPL", "Apple")
        self.assertEqual(sm.Stock.create("AAPL", "Apple").to_dict(), data)

    def test_create_false(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(sm.Stock.create("AAPL", "Apple"), False)

    def test_update_true(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (1, "AAPL", "Apple")
        pool_manager.return_value.__exit__.return_value = True
        self.assertEqual(sm.Stock(1, 'IBM', 'IBM').update(name="AAPL", company_name="Apple"), True)

    def test_update_false(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(sm.Stock(1, 'IBM', 'IBM').update(name="AAPL", company_name="Apple"), False)

    @patch('stock_dashboard_api.models.stock_model.Stock.get_by_id')
    def test_delete_true(self, get_by_id, pool_manager):
        get_by_id.return_value = True
        pool_manager.return_value.__enter__.return_value.cursor.execute.return_value = True
        self.assertEqual(sm.Stock.delete_by_id(1), True)

    @patch('stock_dashboard_api.models.stock_model.Stock.get_by_id')
    def test_delete_id_not_exist(self, get_by_id, pool_manager):
        get_by_id.return_value = False
        pool_manager.return_value.__enter__.return_value.cursor.execute.return_value = True
        self.assertEqual(sm.Stock.delete_by_id(1), False)

    @patch('stock_dashboard_api.models.stock_model.Stock.get_by_id')
    def test_delete_error(self, get_by_id, pool_manager):
        get_by_id.return_value = True
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(sm.Stock.delete_by_id(1), False)

    def test_get_by_id(self, pool_manager):
        data = {"id": 1, "name": "AAPL", "company_name": "Apple"}
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (1, "AAPL", "Apple")
        self.assertEqual(sm.Stock.get_by_id(1).to_dict(), data)

    def test_get_by_id_error(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(sm.Stock.get_by_id(1), None)


if __name__ == '__main__':
    unittest.main()

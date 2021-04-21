import unittest
from unittest.mock import patch
from datetime import datetime
import psycopg2

from stock_dashboard_api.models.stock_data_models import StockData


@patch('stock_dashboard_api.models.stock_data_models.pool_manager')
class TestStockDataModel(unittest.TestCase):
    def test_create_true(self, pool_manager):
        data = {"id": 1, "stock_id": 1, "price": 441.5, "created_at": datetime(2021, 1, 2, 3, 4, 5)}
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (1, 1, 441.5, datetime(2021, 1, 2, 3, 4, 5))
        self.assertEqual(StockData.create(1, 441.5, datetime(2021, 1, 2, 3, 4, 5)).to_dict(), data)

    def test_create_false(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(StockData.create(1, 441.5, datetime(2021, 1, 2, 3, 4, 5)), None)

    def test_update_true(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (2, 1, 441.5, datetime(2021, 1, 2, 3, 4, 5))
        pool_manager.return_value.__exit__.return_value = True
        self.assertEqual(StockData(1, 111.1, datetime(2020, 3, 2, 1, 5, 6)).update(441.5, datetime(2021, 1, 2, 3, 4, 5)), True)

    def test_update_false(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(StockData(2, 114.6, datetime(2020, 1, 2, 3, 4, 5)).update(441.5, datetime(2021, 1, 2, 3, 4, 5)), False)

    def test_get_by_id(self, pool_manager):
        data = {"id": 1, "stock_id": 1, "price": 441.5, "created_at": datetime(2021, 1, 2, 3, 4, 6)}
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (1, 1, 441.5, datetime(2021, 1, 2, 3, 4, 6))
        self.assertEqual(StockData.get_by_id(1).to_dict(), data)

    def test_get_by_id_error(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(StockData.get_by_id(1), None)

    @patch('stock_dashboard_api.models.stock_data_models.StockData.get_by_id')
    def test_delete_true(self, get_by_id, pool_manager):
        get_by_id.return_value = True
        pool_manager.return_value.__enter__.return_value.cursor.execute.return_value = True
        self.assertEqual(StockData.delete_by_id(1), True)

    @patch('stock_dashboard_api.models.stock_model.Stock.get_by_id')
    def test_delete_error(self, get_by_id, pool_manager):
        get_by_id.return_value = True
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(StockData.delete_by_id(1), False)


if __name__ == '__main__':
    unittest.main()

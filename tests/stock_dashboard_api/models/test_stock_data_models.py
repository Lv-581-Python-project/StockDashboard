from stock_dashboard_api.models.stock_data_models import StockData
import unittest
from unittest.mock import patch
from datetime import datetime


class TestStockDataModels(unittest.TestCase):
    def setUp(self) -> None:
        self.patcher = patch('stock_dashboard_api.models.stock_data_models.StockData', autospec=True).start()
        self.addCleanup(patch.stopall)

    def test_create(self):
        id, stock_id, price, create_at = 1, 2, 121.2, datetime(2020, 1, 2, 2, 1, 3)
        create = self.patcher.create


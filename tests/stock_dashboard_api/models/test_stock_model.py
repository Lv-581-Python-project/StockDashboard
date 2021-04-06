import unittest
from unittest.mock import patch
from stock_dashboard_api.models import stock_model as sm

@patch('stock_dashboard_api.models.stocks_models.pool_manager', **{'method.return_value': 3})
class TestStock(unittest.TestCase):
    def test_create(self, pool_manager):
        data = {"id": 1, "name": "AAPL", "company_name": "Apple"}
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (1,"AAPL", "Apple")

        self.assertEqual(sm.Stock.create("AAPL", "Apple"), data)

    def test_update(self, pool_manager):
        data = {"id": 1, "name": "AAPL", "company_name": "Apple"}
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (1, "AAPL", "Apple")
        self.assertEqual(sm.Stock.update("AAPL", "Apple"), data)




if __name__ == '__main__':
    unittest.main()






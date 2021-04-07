import unittest
from unittest.mock import patch
from stock_dashboard_api.models import stock_model as sm

inst = sm.Stock(1,'2323','2323')


@patch('stock_dashboard_api.models.stock_model.pool_manager')
class TestStock(unittest.TestCase):

    def test_create_true(self, pool_manager):
        data = {"id": 1, "name": "AAPL", "company_name": "Apple"}
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (1,"AAPL", "Apple")
        self.assertEqual(sm.Stock.create("AAPL", "Apple").to_dict(), data)


    def test_update(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (1,"AAPL", "Apple")
        pool_manager.return_value.__exit__.return_value= True
        self.assertEqual(sm.Stock(1,'IBM','IBM').update(name="AAPL", company_name="Apple"), True)


    def test_delete(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.__exit__.return_value = True
        self.assertEqual(sm.Stock.delete_by_id(1), True)

    def test_get_by_id(self, pool_manager):
        data = {"id": 1, "name": "AAPL", "company_name": "Apple"}
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (1,"AAPL", "Apple")
        self.assertEqual(sm.Stock.get_by_id(1).to_dict(), data)




if __name__ == '__main__':
    unittest.main()






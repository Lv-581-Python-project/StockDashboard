import datetime
import unittest
from unittest.mock import patch

import psycopg2

from stock_dashboard_api.models import stock_model as sm
from stock_dashboard_api.models.stock_data_models import StockData


@patch('stock_dashboard_api.models.stock_model.pool_manager')
class TestStock(unittest.TestCase):

    def test_create_true(self, pool_manager):
        data = {"id": 1, "name": "AAPL", "company_name": "Apple", "country": "United States", "industry": "Computer Manufacturing", "sector": "Technology", "in_use": False}
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (1, "AAPL", "Apple", "United States", "Computer Manufacturing", "Technology", False)
        self.assertEqual(sm.Stock.create("AAPL", "Apple", "United States", "Computer Manufacturing", "Technology").to_dict(), data)

    def test_create_false(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(sm.Stock.create("AAPL", "Apple", "United States", "Computer Manufacturing", "Technology"), None)

    def test_update_true(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (1, "AAPL", "Apple", "United States", "Computer Manufacturing", "Technology", False)
        pool_manager.return_value.__exit__.return_value = True
        self.assertEqual(sm.Stock('IBM', 'IBM', "United States", "Computer Manufacturing", "Technology").update(name="AAPL",
                                                                                                                company_name="Apple",
                                                                                                                country="United States",
                                                                                                                industry="Computer Manufacturing",
                                                                                                                sector="Technology"), True)

    def test_update_false(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(sm.Stock('IBM', 'IBM', "United States", "Computer Manufacturing", "Technology").update(name="AAPL",
                                                                                                                company_name="Apple",
                                                                                                                country="United States",
                                                                                                                industry="Computer Manufacturing",
                                                                                                                sector="Technology"), False)

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
        data = {"id": 1, "name": "AAPL", "company_name": "Apple", "country": "United States", "industry": "Computer Manufacturing", "sector": "Technology", "in_use": False}
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (1, "AAPL", "Apple", "United States", "Computer Manufacturing", "Technology", False)
        self.assertEqual(sm.Stock.get_by_id(1).to_dict(), data)

    def test_get_by_id_error(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(sm.Stock.get_by_id(1), None)

    def test_get_data_for_time_period(self, pool_manager):
        datetime_from, datetime_to = datetime.datetime(2020, 4, 1, 5, 21, 45), datetime.datetime(2020, 4, 1, 5, 22, 30)
        stock_data_id, stock_id, stock_data_price = 1, 1, 144.15
        stock_data_created_at = datetime.datetime(2020, 4, 1, 5, 21, 22)
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (stock_id,
                                                                                         "AAPL",
                                                                                         "Apple",
                                                                                         "United States",
                                                                                         "Computer Manufacturing",
                                                                                         "Technology",
                                                                                         False)
        stock = sm.Stock.get_by_id(1)
        pool_manager.return_value.__enter__.return_value.cursor.fetchall.return_value = [(stock_data_id,
                                                                                          stock_id,
                                                                                          stock_data_price,
                                                                                          stock_data_created_at), ]
        stock_data_for_time_period = stock.get_data_for_time_period(datetime_from, datetime_to)
        stock_data_for_time_period_dict = [stock.to_dict() for stock in stock_data_for_time_period]
        expected_result = [{'id': stock_data_id,
                            'stock_id': stock_id,
                            'price': stock_data_price,
                            'created_at': stock_data_created_at}, ]

        self.assertEqual(expected_result, stock_data_for_time_period_dict)

    def test_junk(self, pool_manager):
        datetime_from, datetime_to = datetime.datetime(2020, 4, 1, 3, 20), datetime.datetime(2020, 4, 1, 8, 20)
        stock_data = [StockData(1, 1.1, datetime.datetime(2020, 4, 1, 5, 30)),
                      StockData(1, 1.1, datetime.datetime(2020, 4, 1, 5, 45)),
                      StockData(1, 1.1, datetime.datetime(2020, 4, 1, 6, 15)),
                      StockData(1, 1.1, datetime.datetime(2020, 4, 1, 7, 30)),]
        print()
        print()
        res = sm.Stock._get_gaps_in_data(datetime_from, datetime_to, stock_data)
        print(res)

    def test_get_data_for_time_period_error(self, pool_manager):
        datetime_from = datetime.datetime(2020, 4, 1, 5, 21, 45)
        datetime_to = datetime.datetime(2020, 4, 1, 5, 22, 30)
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = TypeError
        self.assertEqual(sm.Stock('IBM', 'IBM', "United States", "Computer Manufacturing", "Technology").get_data_for_time_period(datetime_from, datetime_to), [])

    def test_get_all(self, pool_manager):
        data = [(1, 'IBM', 'IBM',  "United States", "Computer Manufacturing", "Technology", False),
                (2, 'AAPL', 'Apple', "United States", "Computer Manufacturing", "Technology", False),
                (3, 'GOOGL', 'Google', 'United States', 'Computer Software: Programming Data Processing', 'Technology', False)]
        expected_pks = [d[0] for d in data]
        expected_names = [d[1] for d in data]
        expected_company_names = [d[2] for d in data]
        expected_countries = [d[3] for d in data]
        expected_industries = [d[4] for d in data]
        expected_sectors = [d[5] for d in data]
        pool_manager.return_value.__enter__.return_value.cursor.fetchall.return_value = data
        stocks = sm.Stock.get_all()
        pks = [stock.pk for stock in stocks]
        names = [stock.name for stock in stocks]
        company_names = [stock.company_name for stock in stocks]
        countries = [stock.country for stock in stocks]
        industries = [stock.industry for stock in stocks]
        sectors = [stock.sector for stock in stocks]

        self.assertEqual(expected_pks, pks)
        self.assertEqual(expected_names, names)
        self.assertEqual(expected_company_names, company_names)
        self.assertEqual(expected_countries, countries)
        self.assertEqual(expected_industries, industries)
        self.assertEqual(expected_sectors, sectors)

    def test_get_all_error(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(sm.Stock.get_all(), [])

    def test_get_gaps(self, pool_manager):
        datetime_from, datetime_to = datetime.datetime(2020, 4, 1, 3, 20), datetime.datetime(2020, 4, 1, 8, 20)
        stock_data = [StockData(1, 1.1, datetime.datetime(2020, 4, 1, 5, 30)),
                      StockData(1, 1.1, datetime.datetime(2020, 4, 1, 5, 45)),
                      StockData(1, 1.1, datetime.datetime(2020, 4, 1, 6, 15)),
                      StockData(1, 1.1, datetime.datetime(2020, 4, 1, 7, 30))]
        expected_result = [(datetime.datetime(2020, 4, 1, 3, 20), datetime.datetime(2020, 4, 1, 5, 30)),
                           (datetime.datetime(2020, 4, 1, 5, 45), datetime.datetime(2020, 4, 1, 6, 15)),
                           (datetime.datetime(2020, 4, 1, 6, 15), datetime.datetime(2020, 4, 1, 7, 30)),
                           (datetime.datetime(2020, 4, 1, 7, 30), datetime.datetime(2020, 4, 1, 8, 20))]
        res = sm.Stock._get_gaps_in_data(datetime_from, datetime_to, stock_data)
        self.assertEqual(expected_result, res)


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch

import workers.utils.daemon_check_new_stocks as daemon


@patch("workers.utils.daemon_check_new_stocks.insert_new_stock")
@patch("workers.utils.daemon_check_new_stocks.get_all_stocks_name")
@patch("workers.utils.daemon_check_new_stocks.requests", autospec=True)
@patch("workers.utils.daemon_check_new_stocks.time", autospec=True)
class TestCheckNewStocks(unittest.TestCase):

    def test_check_new_stocks(self, time, requests, get, insert):
        get.return_value = {'AAPL', 'TSLA'}
        requests.get.return_value.json.return_value = {'data': {'rows': [{'symbol': 'AAPL'}]}}
        daemon.check_new_stocks()
        self.assertTrue(time.sleep.called)

    def test_save_new_stocks(self, time, requests, get, insert):
        insert.return_value = True
        requests.get.return_value.json.return_value = {'data': {'rows': [
            {'symbol': 'AAPL', 'name': 'Apple', 'country': 'United States', 'industry': 'Computer Manufacturing',
             'sector': 'Technology'}]}}
        self.assertTrue(daemon.save_new_stock_data('AAPL'))

    def test_bad_save_new_stocks(self, time, requests, get, insert):
        insert.return_value = False
        requests.get.return_value.json.return_value = {
            'data': {
                'rows': [
                    {
                        'symbol': 'AAPL',
                        'name': 'Apple',
                        'country': 'United States',
                        'industry': 'Computer Manufacturing',
                        'sector': 'Technology'
                    }
                ]
            }
        }
        self.assertTrue(daemon.save_new_stock_data('AAPL'))

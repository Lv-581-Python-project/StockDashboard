import datetime
import unittest
from unittest.mock import patch

import workers.utils.daemon_for_updating_stocks as daemon


@patch("workers.utils.daemon_for_updating_stocks.get_all_stocks_in_use")
@patch("workers.utils.daemon_for_updating_stocks.get_stocks_data_last_record")
@patch("workers.utils.daemon_for_updating_stocks.data_for_stocks_data_update")
@patch("workers.utils.daemon_for_updating_stocks.publish_task")
@patch("workers.utils.daemon_for_updating_stocks.time")
class TestUpdatingStocks(unittest.TestCase):
    def test_updating_stocks(self, time, pb, stocks_update, stocks_last_record, stock_in_use):
        stock_in_use.return_value = [{'id': 1, 'name': 'AAPL'}]
        stocks_last_record.return_value = datetime.datetime.now()
        stocks_update.return_value = [{
            'queue': 'get_stock_data_queue',
            'stock_id': 1,
            'price': 127,
            'created_at': str(datetime.datetime.now())
        }]
        daemon.updating_stocks()
        self.assertTrue(time.sleep.called)

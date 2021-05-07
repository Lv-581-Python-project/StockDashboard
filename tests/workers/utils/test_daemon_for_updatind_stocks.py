import datetime
import unittest
from unittest.mock import patch

import workers.utils.daemon_for_updating_stocks as daemon


@patch("workers.utils.daemon_for_updating_stocks.get_all_stocks_in_use")
@patch("workers.utils.daemon_for_updating_stocks.publish_task")
@patch("workers.utils.daemon_for_updating_stocks.time")
class TestUpdatingStocks(unittest.TestCase):
    def test_updating_stocks(self, time, publish_task, stock_in_use):
        stock_in_use.return_value = [{'id': 1, 'name': 'AAPL'}]
        publish_task.return_value
        daemon.updating_stocks()
        self.assertTrue(time.sleep.called)

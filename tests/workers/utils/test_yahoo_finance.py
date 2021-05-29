import unittest
from unittest.mock import patch

import workers.utils.yahoo_finance as yahoo_finance


@patch("workers.utils.yahoo_finance.yf", autospec=True)
class TestYahooFinanceApi(unittest.TestCase):
    def test_if_exist_true(self, yf):
        yf.Ticker.return_value.info = {'name': 'name', 'company_name': 'company_name'}
        self.assertTrue(yahoo_finance.check_if_exist('AAPL'))

    def test_if_exist_false(self, yf):
        yf.Ticker.return_value.info = {'name': 'name'}
        self.assertFalse(yahoo_finance.check_if_exist('AAPLA'))

    @patch("workers.utils.yahoo_finance.datetime", autospec=True)
    def test_data_for_stocks(self, datetime, yf):
        data = [
            {
                'created_at': '2022',
                'price': 125.70999908447266
            }
        ]
        datetime.datetime.now.return_value.astimezone.return_value = 2022
        yf.Ticker.return_value.history.return_value.itertuples.return_value = (
            (datetime.datetime.now(), 2, 125.70999908447266),
        )
        self.assertEqual(yahoo_finance.data_for_stocks_data_update('AAPL', 2021, 2022), data)

    def test_get_meta_data(self, yf):
        data = {
            'name': 'AACG',
            'company_name': 'ATA Creativity Global',
            'country': 'China',
            'industry': 'Education & Training Services',
            'sector': 'Consumer Defensive'
        }

        yf.Ticker.return_value.info = {
            'name': 'AACG',
            'longName': 'ATA Creativity Global',
            'country': 'China',
            'industry': 'Education & Training Services',
            'sector': 'Consumer Defensive'
        }
        self.assertEqual(yahoo_finance.get_meta_data('AACG'), data)

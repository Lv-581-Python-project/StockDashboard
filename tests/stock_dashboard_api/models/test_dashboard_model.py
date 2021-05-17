import unittest
from unittest.mock import patch

import psycopg2

from stock_dashboard_api.models import dashboard_model
from stock_dashboard_api.models.stock_model import Stock

FETCH_ONE_RETURN_VALUE = ('TESTHASH',)


@patch('stock_dashboard_api.models.dashboard_model.pool_manager')
class TestStock(unittest.TestCase):

    def test_create_true(self, pool_manager):
        data = {"dashboard_hash": "TESTHASH"}
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = FETCH_ONE_RETURN_VALUE
        self.assertDictEqual(dashboard_model.Dashboard.create(
            [Stock(pk=1,
                   name="A",
                   company_name="Agilent Technologies Inc. Common Stock",
                   country='United States',
                   industry='Biotechnology: Laboratory Analytical Instruments',
                   sector='Capital Goods',
                   in_use=False)]).to_dict(), data)

    def test_create_fail(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(dashboard_model.Dashboard.create(
            [Stock(pk=1,
                   name="A",
                   company_name="Agilent Technologies Inc. Common Stock",
                   country='United States',
                   industry='Biotechnology: Laboratory Analytical Instruments',
                   sector='Capital Goods',
                   in_use=False)]), None)

    def test_update_true(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = FETCH_ONE_RETURN_VALUE
        pool_manager.return_value.__exit__.return_value = True
        self.assertEqual(dashboard_model.Dashboard('TESTHASH').update(dashboard_hash='HASHTEST'), True)

    def test_update_false(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(dashboard_model.Dashboard('TESTHASH').update(dashboard_hash='HASHTEST'), None)

    @patch('stock_dashboard_api.models.dashboard_model.Dashboard.get_by_hash')
    def test_delete_true(self, get_by_hash, pool_manager):
        get_by_hash.return_value = True
        pool_manager.return_value.__enter__.return_value.cursor.execute.return_value = True
        self.assertEqual(dashboard_model.Dashboard.delete_by_hash("TESTHASH"), True)

    @patch('stock_dashboard_api.models.dashboard_model.Dashboard.get_by_hash')
    def test_delete_error(self, get_by_hash, pool_manager):
        get_by_hash.return_value = True
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(dashboard_model.Dashboard.delete_by_hash("TESTHASH"), None)

    def test_get_by_hash_pass(self, pool_manager):
        data = {"dashboard_hash": 'TESTHASH'}
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = FETCH_ONE_RETURN_VALUE
        self.assertDictEqual(dashboard_model.Dashboard.get_by_hash('TESTHASH').to_dict(), data)

    def test_get_by_hash_fail(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(dashboard_model.Dashboard.get_by_hash(1), None)

    def test_get_stocks_pass(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.fetchall.return_value = [
            (1, "A", "Agilent Technologies Inc. Common Stock", 'United States', 'Biotechnology: Laboratory Analytical Instruments', 'Capital Goods', False)]
        self.assertEqual(dashboard_model.Dashboard("TESTHASH").get_stocks()[0].pk,
                         Stock(pk=1,
                               name="A",
                               company_name="Agilent Technologies Inc. Common Stock",
                               country='United States',
                               industry='Biotechnology: Laboratory Analytical Instruments',
                               sector='Capital Goods',
                               in_use=False).pk)

    def test_get_stocks_fail(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.ProgrammingError
        self.assertEqual(dashboard_model.Dashboard("TESTHASH").get_stocks(), None)

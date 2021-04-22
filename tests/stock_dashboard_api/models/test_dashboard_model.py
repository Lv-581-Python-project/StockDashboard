import unittest
from unittest.mock import patch

import psycopg2

from stock_dashboard_api.models import dashboard_model


@patch('stock_dashboard_api.models.dashboard_model.pool_manager')
class TestStock(unittest.TestCase):

    def test_create_true(self, pool_manager):
        data = {"pk": 1, "config_hash": "TESTHASH"}
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (1, 'TESTHASH')
        self.assertDictEqual(dashboard_model.Dashboard.create(config_hash="TESTHASH").to_dict(), data)

    def test_create_fail(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(dashboard_model.Dashboard.create('TESTHASH'), False)

    def test_update_true(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (1, 'TESTHASH')
        pool_manager.return_value.__exit__.return_value = True
        self.assertEqual(dashboard_model.Dashboard('TESTHASH').update(config_hash='HASHTEST'), True)

    def test_update_false(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(dashboard_model.Dashboard('TESTHASH').update(config_hash='HASHTEST'), False)

    @patch('stock_dashboard_api.models.dashboard_model.Dashboard.get_by_id')
    def test_delete_true(self, get_by_id, pool_manager):
        get_by_id.return_value = True
        pool_manager.return_value.__enter__.return_value.cursor.execute.return_value = True
        self.assertEqual(dashboard_model.Dashboard.delete_by_id(1), True)

    @patch('stock_dashboard_api.models.dashboard_model.Dashboard.get_by_id')
    def test_delete_id_does_not_exist(self, get_by_id, pool_manager):
        get_by_id.return_value = False
        pool_manager.return_value.__enter__.return_value.cursor.execute.return_value = True
        self.assertEqual(dashboard_model.Dashboard.delete_by_id(1), False)

    @patch('stock_dashboard_api.models.dashboard_model.Dashboard.get_by_id')
    def test_delete_error(self, get_by_id, pool_manager):
        get_by_id.return_value = True
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(dashboard_model.Dashboard.delete_by_id(1), False)

    def test_get_by_id(self, pool_manager):
        data = {"pk": 1, "config_hash": 'TESTHASH'}
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (1, 'TESTHASH')
        self.assertDictEqual(dashboard_model.Dashboard.get_by_id(1).to_dict(), data)

    def test_get_by_id_error(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(dashboard_model.Dashboard.get_by_id(1), None)

    def test_get_by_hash_pass(self, pool_manager):
        data = {"pk": 1, "config_hash": 'TESTHASH'}
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (1, 'TESTHASH')
        self.assertDictEqual(dashboard_model.Dashboard.get_by_hash('TESTHASH').to_dict(), data)

    def test_get_by_hash_fail(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(dashboard_model.Dashboard.get_by_hash(1), None)

    def test_get_all_hashes(self, pool_manager):
        data = ["TESTSADF", "TESTSAD1", "TESTSAD2", "TESTSAD3", "TESTSAD4", "TESTSAD5"]
        pool_manager.return_value.__enter__.return_value.cursor.fetchall.return_value = [("TESTSADF",), ("TESTSAD1",),
                                                                                         ("TESTSAD2",), ("TESTSAD3",),
                                                                                         ("TESTSAD4",), ("TESTSAD5",)]
        self.assertEqual(dashboard_model.Dashboard.get_all_hashes(), data)

    def test_get_all_hashes_error(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.ProgrammingError
        self.assertEqual(dashboard_model.Dashboard.get_all_hashes(), None)

    def test_get_stocks_pass(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.fetchall.return_value = [(1,), (2,), (3,), (4,)]
        self.assertEqual(dashboard_model.Dashboard(1, "TESTHASH").get_stocks(), [1, 2, 3, 4])

    def test_get_stocks_fail(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.ProgrammingError
        self.assertEqual(dashboard_model.Dashboard(1, "TESTHASH").get_stocks(), None)

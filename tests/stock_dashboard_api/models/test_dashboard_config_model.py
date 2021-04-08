import unittest
from unittest.mock import patch

import psycopg2

from stock_dashboard_api.models import dashboard_config_model


@patch('stock_dashboard_api.models.dashboard_config_model.pool_manager')
class TestStock(unittest.TestCase):

    def test_create_true(self, pool_manager):
        data = {"pk": 1, "config_hash": "TESTHASH"}
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (1, 'TESTHASH')
        self.assertDictEqual(dashboard_config_model.DashboardConfig.create(config_hash="TESTHASH").to_dict(), data)

    def test_create_fail(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(dashboard_config_model.DashboardConfig.create('TESTHASH'), False)

    def test_update_true(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (1, 'TESTHASH')
        pool_manager.return_value.__exit__.return_value = True
        self.assertEqual(dashboard_config_model.DashboardConfig('TESTHASH').update(config_hash='HASHTEST'), True)

    def test_update_false(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(dashboard_config_model.DashboardConfig('TESTHASH').update(config_hash='HASHTEST'), False)

    @patch('stock_dashboard_api.models.dashboard_config_model.DashboardConfig.get_by_id')
    def test_delete_true(self, get_by_id, pool_manager):
        get_by_id.return_value = True
        pool_manager.return_value.__enter__.return_value.cursor.execute.return_value = True
        self.assertEqual(dashboard_config_model.DashboardConfig.delete_by_id(1), True)

    @patch('stock_dashboard_api.models.dashboard_config_model.DashboardConfig.get_by_id')
    def test_delete_id_does_not_exist(self, get_by_id, pool_manager):
        get_by_id.return_value = False
        pool_manager.return_value.__enter__.return_value.cursor.execute.return_value = True
        self.assertEqual(dashboard_config_model.DashboardConfig.delete_by_id(1), False)

    @patch('stock_dashboard_api.models.dashboard_config_model.DashboardConfig.get_by_id')
    def test_delete_error(self, get_by_id, pool_manager):
        get_by_id.return_value = True
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(dashboard_config_model.DashboardConfig.delete_by_id(1), False)

    def test_get_by_id(self, pool_manager):
        data = {"pk": 1, "config_hash": 'TESTHASH'}
        pool_manager.return_value.__enter__.return_value.cursor.fetchone.return_value = (1, 'TESTHASH')
        self.assertDictEqual(dashboard_config_model.DashboardConfig.get_by_id(1).to_dict(), data)

    def test_get_by_id_error(self, pool_manager):
        pool_manager.return_value.__enter__.return_value.cursor.execute.side_effect = psycopg2.DataError
        self.assertEqual(dashboard_config_model.DashboardConfig.get_by_id(1), None)

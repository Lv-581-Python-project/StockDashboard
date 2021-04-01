from stock_dashboard_api.models.dashboard_config_models import DashboardConfig


new_config = DashboardConfig.create(config_hash='hashconf')
print('CREATED OBJECT')
config = DashboardConfig.get_by_id(new_config.pk)
print(config, 'GOT OBJECT')
config.update(config_hash='confhash')
print(config, 'UPDATED OBJECT')
DashboardConfig.delete_by_id(1)
print(config, 'DELETED OBJECT')

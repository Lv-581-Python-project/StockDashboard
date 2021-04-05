from stock_dashboard_api.models.stocks_data_models import StockData
from datetime import datetime


# StockData.delete_by_id(22)
# StockData.delete_by_id(14)
# StockData.delete_by_id(13)
# StockData.create(5, 555.55, datetime(2016, 2, 5, 11, 14, 52))
StockData.get_by_id(9).update(999.99, datetime(2011, 11, 11, 11, 11, 11))





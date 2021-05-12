import json
import time

from workers.utils.db_service import get_all_stocks_in_use
from workers.utils.scheduler_queue import publish_task

UPDATING_TIME = 15 * 60
QUEUE = 'get_stock_data_queue'


def updating_stocks():
    """
    Send new data for updating stocks to queue every 15 min

    """
    all_stocks_in_use = get_all_stocks_in_use()

    for stock in all_stocks_in_use:
        body = json.dumps({'queue': QUEUE, 'stock_id': stock['id'], 'name': stock['name']})
        publish_task(body)


if __name__ == '__main__':
    while True:
        updating_stocks()
        time.sleep(UPDATING_TIME)

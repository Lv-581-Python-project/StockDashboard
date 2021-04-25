import json
import time

from workers.utils.db_service import get_all_stocks_in_use, get_stocks_data_last_record
from workers.utils.scheduler_queue import publish_task
from workers.utils.yahoo_finance import data_for_stocks_data_update

UPDATING_TIME = 900
URL = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true"
HEADER = {
    'user-agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
}


def updating_stocks():
    all_stocks_in_use = get_all_stocks_in_use()
    for stock in all_stocks_in_use:
        stock_id = stock['id']
        name = stock['name']
        start = get_stocks_data_last_record(stock_id)
        data_for_update = data_for_stocks_data_update(stock_id, name, start)
        for data in data_for_update:
            body = json.dumps(data)
            publish_task(body)

    time.sleep(UPDATING_TIME)


if __name__ == '__main__':
    while True:
        updating_stocks()

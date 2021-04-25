import datetime

import yfinance as yf

DELAY = 10
PRICE_INDEX = 2
DATE_INDEX = 0
QUEUE = 'get_stock_data_queue'


def check_if_exist(ticket):
    all_info = yf.Ticker(ticket)
    if len(all_info.info) == 1:
        return False
    return True


def data_for_stocks_data_update(stock_id, name, start):
    if check_if_exist(name):
        data_for_update = []
        data = yf.Ticker(name).history(start=start, end=datetime.datetime.now(), interval='15m')
        for raw in data.itertuples():
            if start >= raw[DATE_INDEX].astimezone(tz=None):
                continue
            data_for_update.append({
                'queue': QUEUE,
                'stock_id': stock_id,
                'price': raw[PRICE_INDEX],
                'created_at': str(raw[DATE_INDEX].astimezone(tz=None))
            })
        return data_for_update
    return False

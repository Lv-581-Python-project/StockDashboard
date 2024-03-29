import datetime

import yfinance as yf

DELAY = 10
PRICE_INDEX = 2
DATE_INDEX = 0
QUEUE = 'get_stock_data_queue'


def check_if_exist(ticket: str) -> bool:
    """
    Chech if exist stock with this name on yahoo finance

    :param ticket: Name of stock
    :return: True, if opertion was successful and False is not
    """
    all_info = yf.Ticker(ticket)
    if len(all_info.info) == 1:
        return False
    return True


def data_for_stocks_data_update(stock_id: int, name: str, start: datetime) -> list or bool:
    """
    Fetch data from yahoo finance

    :param stock_id: stock id from stocks table
    :param name: stock name
    :param start: last record date from stocks_data
    :return: list with data if opertion was successful and False if not
    """
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


def get_meta_data(name: str) -> dict:
    """
    Fetch meta data for stocks from yahoo finance
    :param name: stock name
    :return: dict with meta data
    """
    data = yf.Ticker(name).info
    return {
        'name': name,
        'company_name': data['longName'],
        'country': data['country'],
        'industry': data['industry'],
        'sector': data['sector']
    }

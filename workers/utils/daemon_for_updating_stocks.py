import time

import requests

from db_service import insert_stock_data
from yahoo_finance import update_stocks_data

UPDATING_DAILY_TIME = 86400
UPDATING_TIME = 900
URL = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true"
HEADER = {
    'user-agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
}

response = requests.get(URL, headers=HEADER)


def get_all_stocks_name():
    return {'TSLA', 'AAPL'}  # return set of name


def get_all_stocks_in_use():
    return [{'id': 1, 'name': 'TSLA', } {'id': 2, 'name': 'AAPL', }]


def get_stocks_data_old_date(stock_id):
    return '1234-12-12'


def get_new_stock_data(ticket):
    for data in response.json()['data']['rows']:
        if data['symbol'] == ticket:
            body = {'name': data['symbol'], 'company_name': data['name'], 'country': data['country'],
                    'industry': data['industry'], 'sector': data['sector']}


def daily_stocks_check():
    while True:
        stocks_from_url = set()
        stocks_from_db = get_all_stocks_name()
        for ticket in response.json()['data']['rows']:
            stocks_from_url.add(ticket['symbol'])
        new_data = stocks_from_url - stocks_from_db
        if len(new_data) != 0:
            for ticket in new_data:
                get_new_stock_data(ticket)
        time.sleep(UPDATING_DAILY_TIME)


def stocks_data_update():
    while True:
        all_in_use = get_all_stocks_in_use()
        for data in all_in_use:
            stock_id = data['id']
            name = data['name']
            start = get_stocks_data_old_date(stock_id)
            data_for_update = update_stocks_data(stock_id, name, start)
            insert_stock_data(data_for_update)
        time.sleep(UPDATING_TIME)
#
# t1 = threading.Thread(target=a)
# t2 = threading.Thread(target=b)
# t1.start()
# t2.start()

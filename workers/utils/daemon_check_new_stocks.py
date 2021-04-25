import time

import requests

from workers.utils.db_service import get_all_stocks_name, insert_new_stock

UPDATING_DAILY_TIME = 86400
URL = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true"
HEADER = {
    'user-agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
}


def save_new_stock_data(ticket):
    response = requests.get(URL, headers=HEADER)
    for data in response.json()['data']['rows']:
        if data['symbol'] == ticket:
            insert_new_stock(data['symbol'], data['name'], data['country'], data['industry'], data['sector'])
            return True


def check_new_stocks():
    stocks_from_url = set()
    stocks_from_db = get_all_stocks_name()
    response = requests.get(URL, headers=HEADER)
    for ticket in response.json()['data']['rows']:
        stocks_from_url.add(ticket['symbol'])
    new_data = stocks_from_url - stocks_from_db
    for ticket in new_data:
        save_new_stock_data(ticket)
    time.sleep(UPDATING_DAILY_TIME)


if __name__ == "__main__":
    while True:
        check_new_stocks()

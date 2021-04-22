import time

import requests
import threading

#from db_service import stocks_counter

UPDATING_DAILY_TIME = 86400
UPDATING_TIME = 900
URL = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true"
HEADER = {
    'user-agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
}

response = requests.get(URL, headers=HEADER)

def get_all_stocks_name():
    return {'TSLA', 'AAPL'}

def get_new_stock_data(ticket):
    for data in response.json()['data']['rows']:
        if data['symbol'] == ticket:
            body = {'name': data['symbol'], 'company_name': data['name'], 'country': data['country'], 'industry': data['industry'], 'sector': data['sector']}
            print(body)


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

        time.sleep(1)
#
# t1 = threading.Thread(target=a)
# t2 = threading.Thread(target=b)
# t1.start()
# t2.start()


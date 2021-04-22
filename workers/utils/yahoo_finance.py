import datetime

import yfinance as yf

from stock_dashboard_api.utils.pool import pool_manager

DELAY = 10


def check_if_exist(ticket):
    all_info = yf.Ticker(ticket)
    if len(all_info.info) == 1:
        raise False
    return True


def update_stocks_data(stock_id, name, start):
    if check_if_exist(name):
        data_for_update = []
        data = yf.Ticker(name).history(start=start, end=datetime.datetime.now(), period='15m')
        for raw in data.itertuples():
            data_for_update.append((stock_id, raw[2], str(raw[0].astimezone(tz=None)))
        return data_for_update


def get_one_ticket(ticket):
    if check_if_exist(ticket):
        all_info = yf.Ticker(ticket)
        name = all_info.info['symbol']
        company_name = all_info.info['shortName']
        ticket_id_in_db = None
        with pool_manager() as conn:
            query = 'INSERT INTO public.stocks(name, company_name) VALUES (%(name)s, %(company_name)s) RETURNING id;'
            ticket_id_in_db = conn.cursor.fetchone()
            conn.cursor.execute(query, {'name': name, 'company_name': company_name})

            data = all_info.history('5d', interval='15m')

            query = 'INSERT INTO public.stocks_data(stock_id, price, create_at) ' \
                    'VALUES (%(stock_id)s, %(price)s, %(create_at)s)'
            for raw in data.itertuples():
                conn.cursor.execute(query, {'stock_id': ticket_id_in_db, 'price': raw[2],
                                            'create_at': raw[0].astimezone(tz=None)})

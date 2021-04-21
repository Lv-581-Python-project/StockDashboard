import time

import requests

from db_service import stocks_counter

UPDATING_TIME = 86400
URL = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true"
HEADER = {
    'user-agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
}

def rmq(body):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ.get('RABBITMQ_CONNECTION_HOST'))
    )
    channel = connection.channel()
    channel.exchange_declare(
        exchange='scheduler',
        exchange_type='direct',
    )
    channel.queue_declare(queue='scheduler_queue', durable=True)
    channel.queue_bind(exchange='scheduler', queue='scheduler_queue')
    channel.basic_publish(
        exchange='scheduler',
        routing_key='scheduler_queue',
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=int(os.environ.get('RABBITMQ_DELIVERY_MODE')),
        )
    )


while True:
    response = requests.get(URL, headers=HEADER)
    counter_from_url = len(response.json()['data']['rows'])
    counter_from_table = stocks_counter()
    if counter_from_url > counter_from_table:
        stocks_from_table = get_all_name() #list with all names from stock table
        for stock_name in response.json()['data']['rows']['symbol']:
            if stock_name not in stocks_from_table:
                rmq(stock_name)



    time.sleep(UPDATING_TIME)

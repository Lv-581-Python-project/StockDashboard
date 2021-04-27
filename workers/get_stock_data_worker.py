import json
import os

import pika

from workers.utils.db_service import get_stocks_data_last_record
from workers.utils.db_service import insert_stock_data
from workers.utils.yahoo_finance import data_for_stocks_data_update


def scheduler_function(ch, method, properties, body):  # pylint: disable=C0103,  W0613
    body = json.loads(body)

    stock_id = body['stock_id']
    name = body['name']
    if 'start' in body:
        start = body['start']
    else:
        start = get_stocks_data_last_record(stock_id)
    data_for_update = data_for_stocks_data_update(stock_id, name, start)
    for data in data_for_update:
        insert_stock_data(data['stock_id'], data['price'], data['created_at'])
    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ.get('RABBITMQ_CONNECTION_HOST'))
    )
    channel = connection.channel()
    channel.queue_declare(queue='get_stock_data_queue', durable=True)
    channel.basic_consume(queue='get_stock_data_queue', on_message_callback=scheduler_function)
    channel.start_consuming()

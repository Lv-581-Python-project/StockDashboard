import json
import os
import time

import pika

from utils.db_service import insert_stock_data
from utils.yahoo_finance import data_for_stocks_data_update


def worker_function(ch, method, properties, body):  # pylint: disable=C0103,  W0613
    body = json.loads(body)
    data = data_for_stocks_data_update(body["stock_name"], body["from"], body["to"])
    for stock in data:
        insert_stock_data(stock["stock_id"], stock["price"], stock["created_at"])
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ.get('RABBITMQ_CONNECTION_HOST'))
    )
    channel = connection.channel()
    channel.queue_declare(queue='worker_queue', durable=True)
    channel.basic_consume(queue='worker_queue', on_message_callback=worker_function)
    channel.start_consuming()

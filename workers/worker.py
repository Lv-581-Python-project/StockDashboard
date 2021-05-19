import json
import os

import pika

from workers.utils.db_service import stock_get_id, insert_stock_data
from workers.utils.yahoo_finance import get_meta_data, data_for_stocks_data_update


def worker_function(ch, method, properties, body):  # pylint: disable=C0103,  W0613
    body = json.loads(body)
    print(body)
    stock_id = stock_get_id(body['stock_name'])
    data = data_for_stocks_data_update(stock_id, body["stock_name"], body["from"], body["to"])
    insert_stock_data(data["stock_id"], body["price"], body["created_at"])

    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ.get('RABBITMQ_CONNECTION_HOST'))
    )
    channel = connection.channel()
    channel.queue_declare(queue='worker_queue', durable=True)
    channel.basic_consume(queue='worker_queue', on_message_callback=worker_function)
    channel.start_consuming()

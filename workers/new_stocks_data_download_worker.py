import os

import pika
import json

from datetime import datetime, timedelta
from workers.utils.yahoo_finance import data_for_stocks_data_update
from workers.utils.db_service import insert_stock_data, stock_get_id


def new_stocks_data_download(ch, method, properties, body):  # pylint: disable=C0103,  W0613
    """
    The scheduler function used to publish tasks to different queues.

    :param ch: channel that the function belongs to.
    :param method: task delivery method.
    :param properties: pika properties.
    :param body: body of the task in json format.
    """
    body = json.loads(body)

    name = body["name"]
    start = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
    id = stock_get_id(name)
    stock_data = data_for_stocks_data_update(id, name, start)
    for data in stock_data:
        insert_stock_data(data['stock_id'], data['price'], data['created_at'])
    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ.get('RABBITMQ_CONNECTION_HOST'))
    )
    channel = connection.channel()
    channel.queue_declare(queue='new_stocks_data_download_queue', durable=True)
    channel.basic_consume(queue='new_stocks_data_download_queue', on_message_callback=new_stocks_data_download)
    channel.start_consuming()

import datetime
import json
import os

import pika

from workers.workers_utils.db_service import insert_stock_data, stock_get_id
from workers.workers_utils.logger import workers_logger as logger
from workers.workers_utils.yahoo_finance import data_for_stocks_data_update


def worker_function(ch, method, properties, body):  # pylint: disable=C0103,  W0613
    body = json.loads(body)
    logger.info(f'Worker Task {body} was received')
    stock_id = stock_get_id(body['stock_name'])
    start = datetime.datetime.fromisoformat(body['from'])
    finish = datetime.datetime.fromisoformat(body['to'])
    data = data_for_stocks_data_update(body["stock_name"], start, finish)
    for stock in data:
        insert_stock_data(stock_id, stock["price"], stock["created_at"])
    logger.info(f'Worker Task {body} was succeseful done')
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ.get('RABBITMQ_CONNECTION_HOST'))
    )
    channel = connection.channel()
    channel.queue_declare(queue='worker_queue', durable=True)
    channel.basic_consume(queue='worker_queue', on_message_callback=worker_function)
    logger.info('Worker connection was created')
    channel.start_consuming()

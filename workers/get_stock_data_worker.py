import json
import os
import sys

import pika

sys.path.append('../workers/utils/')
from workers.utils.db_service import insert_stock_data


def scheduler_function(ch, method, properties, body):  # pylint: disable=C0103,  W0613
    body = json.loads(body)
    print(body)
    insert_stock_data(body['stock_id'], body['price'], body['created_at'])
    print('INSERT DONE')
    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    print('Get stock data worker was started')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ.get('RABBITMQ_CONNECTION_HOST'))
    )
    channel = connection.channel()
    channel.queue_declare(queue='get_stock_data_queue', durable=True)
    channel.basic_consume(queue='get_stock_data_queue', on_message_callback=scheduler_function)
    channel.start_consuming()

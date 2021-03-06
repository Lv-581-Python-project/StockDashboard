import os

import pika
import json


def get_stock_data(ch, method, properties, body):  # pylint: disable=C0103,  W0613
    """
    The scheduler function used to publish tasks to different queues.

    :param ch: channel that the function belongs to.
    :param method: task delivery method.
    :param properties: pika properties.
    :param body: body of the task in json format.
    """
    body = json.loads(body)
    print(body)
    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ.get('RABBITMQ_CONNECTION_HOST'))
    )
    channel = connection.channel()
    channel.queue_declare(queue='get_stock_data_queue', durable=True)
    channel.basic_consume(queue='get_stock_data_queue', on_message_callback=get_stock_data)
    channel.start_consuming()

import os

import pika
import json

from stock_dashboard_api.utils.queue1 import publish_queue1_task
from stock_dashboard_api.utils.queue2 import publish_queue2_task


def scheduler_function(ch, method, properties, body):  # pylint: disable=C0103,  W0613
    dict_body = json.loads(body)
    queue = dict_body['queue']
    if queue == 'queue1':
        publish_queue1_task(body)
    elif queue == 'queue2':
        publish_queue2_task(body)
    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ.get('RABBITMQ_CONNECTION_HOST'))
    )
    channel = connection.channel()
    channel.queue_declare(queue='scheduler_queue', durable=True)
    channel.basic_consume(queue='scheduler_queue', on_message_callback=scheduler_function)
    channel.start_consuming()

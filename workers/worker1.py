import os

import pika
import json


def scheduler_function(ch, method, properties, body):  # pylint: disable=C0103,  W0613
    body = json.loads(body)
    print(body)
    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ.get('RABBITMQ_CONNECTION_HOST'))
    )
    channel = connection.channel()
    channel.queue_declare(queue='queue1_queue', durable=True)
    channel.basic_consume(queue='queue1_queue', on_message_callback=scheduler_function)
    channel.start_consuming()

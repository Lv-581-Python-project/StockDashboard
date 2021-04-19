import os

import pika
import json


def connect_queue():
    """
    Connects to the RMQ server.
    """
    rabbitmq = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ.get('RABBITMQ_CONNECTION_HOST'))
    )
    return rabbitmq


def get_queue1():
    """
    Returns a created email queue.
    """
    connect = connect_queue()
    channel = connect.channel()
    channel.exchange_declare(
        exchange='queue1',
        exchange_type='direct',
    )
    channel.queue_declare(queue='queue1_queue', durable=True)
    channel.queue_bind(exchange='queue1', queue='queue1_queue')
    email_queue = channel
    return email_queue


def get_queue2():
    """
    Returns a created email queue.
    """
    connect = connect_queue()
    channel = connect.channel()
    channel.exchange_declare(
        exchange='queue2',
        exchange_type='direct',
    )
    channel.queue_declare(queue='queue2_queue', durable=True)
    channel.queue_bind(exchange='queue2', queue='queue2_queue')
    email_queue = channel
    return email_queue


def publish_queue1_task(body):
    queue = get_queue1()
    queue.basic_publish(
        exchange='queue1',
        routing_key='queue1_queue',
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=int(os.environ.get('RABBITMQ_DELIVERY_MODE')),
        )
    )


def publish_queue2_task(body):
    queue = get_queue2()
    queue.basic_publish(
        exchange='queue2',
        routing_key='queue2_queue',
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=int(os.environ.get('RABBITMQ_DELIVERY_MODE')),
        )
    )


def scheduler_function(ch, method, properties, body):  # pylint: disable=C0103,  W0613
    dict_body = json.loads(body)
    queue = dict_body['queue']
    if queue == 'queue1':
        publish_queue1_task(body)
    elif queue == 'queue2':
        publish_queue2_task(body)
    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    connection = connect_queue()
    channel = connection.channel()
    channel.queue_declare(queue='scheduler_queue', durable=True)
    channel.basic_consume(queue='scheduler_queue', on_message_callback=scheduler_function)
    channel.start_consuming()

import os

import pika


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

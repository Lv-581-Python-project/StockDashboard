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


def get_worker_queue():
    """
    Returns a created email queue.
    """
    connect = connect_queue()
    channel = connect.channel()
    channel.exchange_declare(
        exchange='worker',
        exchange_type='direct',
    )
    channel.queue_declare(queue='worker_queue', durable=True)
    channel.queue_bind(exchange='worker', queue='worker_queue')
    queue = channel
    return queue


def worker_publish_task(body):
    queue = get_worker_queue()
    queue.basic_publish(
        exchange='worker',
        routing_key='worker_queue',
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=int(os.environ.get('RABBITMQ_DELIVERY_MODE')),
        )
    )

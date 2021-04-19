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

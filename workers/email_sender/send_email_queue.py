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


def get_email_queue():
    """
    Returns a created email queue.
    """
    connect = connect_queue()
    channel = connect.channel()
    channel.exchange_declare(
        exchange='emails',
        exchange_type='direct',
    )
    channel.queue_declare(queue='email_queue', durable=True)
    channel.queue_bind(exchange='emails', queue='email_queue')
    email_queue = channel
    return email_queue


def publish_email(body):
    queue = get_email_queue()
    queue.basic_publish(
        exchange='emails',
        routing_key='email_queue',
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=int(os.environ.get('RABBITMQ_DELIVERY_MODE')),
        )
    )

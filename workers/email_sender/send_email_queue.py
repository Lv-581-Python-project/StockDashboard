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
        exchange='email',
        exchange_type='direct',
        durable=True,
        auto_delete=True,
        internal=True
    )
    channel.queue_declare(queue='email_queue', durable=True)
    channel.queue_bind(exchange='email', queue='email_queue')
    email_queue = channel
    return email_queue

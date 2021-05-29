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


def get_scheduler_queue():
    """
    Returns a created email queue.
    """
    connect = connect_queue()
    channel = connect.channel()
    channel.exchange_declare(
        exchange='scheduler',
        exchange_type='direct',
    )
    channel.queue_declare(queue='scheduler_queue', durable=True)
    channel.queue_bind(exchange='scheduler', queue='scheduler_queue')
    queue = channel
    return queue


def scheduler_publish_task(body):
    """
    A function to publish a task to scheduler queue.

    :param body: body of the task in json format.
    """
    queue = get_scheduler_queue()
    queue.basic_publish(
        exchange='scheduler',
        routing_key='scheduler_queue',
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=int(os.environ.get('RABBITMQ_DELIVERY_MODE')),
        )
    )

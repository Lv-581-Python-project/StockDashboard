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


def get_stock_names_queue():
    """
    Returns a created email queue.
    """
    connect = connect_queue()
    channel = connect.channel()
    channel.exchange_declare(
        exchange='get_stock_names_exchange',
        exchange_type='direct',
    )
    channel.queue_declare(queue='get_stock_names_queue', durable=True)
    channel.queue_bind(exchange='get_stock_names_exchange', queue='get_stock_names_queue')
    email_queue = channel
    return email_queue


def get_stock_data_queue():
    """
    Returns a created email queue.
    """
    connect = connect_queue()
    channel = connect.channel()
    channel.exchange_declare(
        exchange='get_stock_data_exchange',
        exchange_type='direct',
    )
    channel.queue_declare(queue='get_stock_data_queue', durable=True)
    channel.queue_bind(exchange='get_stock_data_exchange', queue='get_stock_data_queue')
    email_queue = channel
    return email_queue


def publish_get_stock_names_task(body):
    queue = get_stock_names_queue()
    queue.basic_publish(
        exchange='get_stock_names_exchange',
        routing_key='get_stock_names_queue',
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=int(os.environ.get('RABBITMQ_DELIVERY_MODE')),
        )
    )


def publish_get_stock_data_task(body):
    queue = get_stock_data_queue()
    queue.basic_publish(
        exchange='get_stock_data_exchange',
        routing_key='get_stock_data_queue',
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=int(os.environ.get('RABBITMQ_DELIVERY_MODE')),
        )
    )


def scheduler_function(ch, method, properties, body):  # pylint: disable=C0103,  W0613
    dict_body = json.loads(body)
    queue = dict_body['queue']
    print(body)
    if queue == 'get_stock_names_queue':
        publish_get_stock_names_task(body)
    elif queue == 'get_stock_data_queue':
        publish_get_stock_data_task(body)
    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    connection = connect_queue()
    channel = connection.channel()
    channel.queue_declare(queue='scheduler_queue', durable=True)
    channel.basic_consume(queue='scheduler_queue', on_message_callback=scheduler_function)
    channel.start_consuming()

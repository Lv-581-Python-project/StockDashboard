import os

import pika
import json


def connect_queue():
    """
    Connects to the RMQ server.

    :return: rabbitmq server.
    """
    rabbitmq = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ.get('RABBITMQ_CONNECTION_HOST'))
    )
    return rabbitmq


def new_stocks_data_download_queue():
    """
    Function to create a get_stock_names queue.

    :return: new_stocks_data_download queue.
    """
    connect = connect_queue()
    channel = connect.channel()
    channel.exchange_declare(
        exchange='new_stocks_data_download_exchange',
        exchange_type='direct',
    )
    channel.queue_declare(queue='new_stocks_data_download_queue', durable=True)
    channel.queue_bind(exchange='new_stocks_data_download_exchange', queue='new_stocks_data_download_queue')
    queue = channel
    return queue


def get_stock_data_queue():
    """
    Returns a created get_stock_data queue.

    :return: get_stock_data queue.
    """
    connect = connect_queue()
    channel = connect.channel()
    channel.exchange_declare(
        exchange='get_stock_data_exchange',
        exchange_type='direct',
    )
    channel.queue_declare(queue='get_stock_data_queue', durable=True)
    channel.queue_bind(exchange='get_stock_data_exchange', queue='get_stock_data_queue')
    queue = channel
    return queue


def new_stocks_data_download_task(body):
    """
    A function to publish a task to get_stock_names queue.

    :param body: body of the task in json format.
    """
    queue = new_stocks_data_download_queue()
    queue.basic_publish(
        exchange='new_stocks_data_download_exchange',
        routing_key='new_stocks_data_download_queue',
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=int(os.environ.get('RABBITMQ_DELIVERY_MODE')),
        )
    )


def publish_get_stock_data_task(body):
    """
    A function to publish a task to get_stock_data queue.

    :param body: body of the task in json format.
    """
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
    """
    The scheduler function used to publish tasks to different queues.

    :param ch: channel that the function belongs to.
    :param method: task delivery method.
    :param properties: pika properties.
    :param body: body of the task in json format.
    """
    dict_body = json.loads(body)
    queue = dict_body['queue']
    print(body)
    if queue == 'new_stocks_data_download_queue':
        new_stocks_data_download_task(body)
    elif queue == 'get_stock_data_queue':
        publish_get_stock_data_task(body)
    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    connection = connect_queue()
    channel = connection.channel()
    channel.queue_declare(queue='scheduler_queue', durable=True)
    channel.basic_consume(queue='scheduler_queue', on_message_callback=scheduler_function)
    channel.start_consuming()

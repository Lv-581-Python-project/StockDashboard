import json
import os
import threading
import time

import pika

from workers.utils.db_service import get_all_stocks_in_use
from workers.worker_queue import worker_publish_task

UPDATING_TIME = 15 * 60


def connect_rmq():
    """
    Connects to the RMQ server.
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ.get('RABBITMQ_CONNECTION_HOST'))
    )
    channel = connection.channel()
    channel.queue_declare(queue='scheduler_queue', durable=True)
    channel.basic_consume(queue='scheduler_queue', on_message_callback=scheduler_function)
    channel.start_consuming()



def scheduler_function(ch, method, properties, body):  # pylint: disable=C0103,  W0613

    worker_publish_task(body)
    dict_body = json.loads(body)
    print(dict_body)
    # queue = dict_body['queue']
    # elif queue == 'get_stock_data_queue':
    #     publish_get_stock_data_task(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def updating_stocks():
    """
    Send new data for updating stocks to queue every 15 min

    """
    while True:
        #all_stocks_in_use = get_all_stocks_in_use()

        # for stock in all_stocks_in_use:
        #     body = json.dumps({'queue': QUEUE, 'stock_id': stock['id'], 'name': stock['name']})
        #     publish_task(body)
        print('start updating stocks')
        time.sleep(10)



if __name__ == '__main__':
    t1 = threading.Thread(target=connect_rmq)
    t2 = threading.Thread(target=updating_stocks)
    t1.start()
    t2.start()


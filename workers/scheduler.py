import datetime
import json
import os
import threading
import time

import pika
from workers.utils.constants import FETCH_DATA_FOR_PERIOD_TASK, FETCH_NEW_STOCK_TASK, FETCH_HISTORICAL_DATA_TASK
from workers.utils.worker_task import Task

from workers.utils.db_service import get_all_stocks_in_use, get_stocks_data_last_record, stock_get_id
from workers.worker_queue import worker_publish_task

UPDATING_TIME = 15 * 60
DEFAULT_PERIOD = os.getenv('DEFAULT_PERIOD_FOR_NEW_STOCK_DATA_DOWNLOAD')


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
    dict_body = json.loads(body)
    if dict_body['task_id'] == 'FETCH_NEW_STOCK_TASK':
        dict_body['task_id'] = FETCH_DATA_FOR_PERIOD_TASK
        body = json.dumps(dict_body)
        worker_publish_task(body)
    elif dict_body['task_id'] == FETCH_HISTORICAL_DATA_TASK:
        dict_body['task_id'] = FETCH_DATA_FOR_PERIOD_TASK
        if (dict_body['to'] - dict_body['from']).total_seconds() > (datetime.timedelta(days=30)).total_seconds():
            pass


    dict_body = json.loads(body)
    print(dict_body)

    ch.basic_ack(delivery_tag=method.delivery_tag)


def updating_stocks():
    """
    Send new data for updating stocks to queue every 15 min

    """
    while True:
        all_stocks_in_use = get_all_stocks_in_use()

        for stock in all_stocks_in_use:
            last_record = get_stocks_data_last_record(stock_get_id(stock))
            worker_publish_task(
                Task(
                    FETCH_DATA_FOR_PERIOD_TASK,
                    stock,
                    date_from=last_record,
                    date_to=datetime.datetime.now()
                )
            )
        time.sleep(UPDATING_TIME)


if __name__ == '__main__':
    t1 = threading.Thread(target=connect_rmq)
    t2 = threading.Thread(target=updating_stocks)
    t1.start()
    t2.start()

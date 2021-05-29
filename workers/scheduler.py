import datetime
import json
import logging
import multiprocessing
import os
import time

import pika

from utils.check_new_stocks import check_new_stocks
from utils.constants import FETCH_DATA_FOR_PERIOD_TASK, FETCH_NEW_STOCK_TASK, FETCH_HISTORICAL_DATA_TASK
from utils.db_service import get_all_stocks_in_use, get_stocks_data_last_record, stock_get_id
from utils.logger import workers_logger as logger
from utils.worker_queue import worker_publish_task
from utils.worker_task import Task

UPDATING_TIME = 15 * 60
UPDATING_DAILY_TIME = 24 * 60 * 60
DEFAULT_PERIOD = int(os.getenv('DEFAULT_PERIOD_FOR_NEW_STOCK_DATA_DOWNLOAD'))

logging.basicConfig(level=logging.DEBUG)


def connect_rmq():
    """
    Connects to the RMQ server.
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ.get('RABBITMQ_CONNECTION_HOST'))
    )
    channel = connection.channel()
    channel.queue_declare(queue='scheduler_queue', durable=True)
    channel.queue_declare(queue='worker_queue', durable=True)
    channel.basic_consume(queue='scheduler_queue', on_message_callback=scheduler_function)
    logger.info('Sheduler connection was created')
    channel.start_consuming()


def fetch_new_stock(data: dict):
    """
    Make task for worker to fetch data about new stock from yahoo finance. Period is default.

    :param data: task template from scheduler queued
    """
    data['task_id'] = FETCH_DATA_FOR_PERIOD_TASK
    data['from'] = (datetime.datetime.now() - datetime.timedelta(days=DEFAULT_PERIOD)).isoformat()
    data['to'] = datetime.datetime.now().isoformat()
    body = json.dumps(data)
    logger.info(f'Send task {data} to workers')
    worker_publish_task(body)


def fetch_historical_data(data: dict):
    """
    Make task for worker to fetch historical data  from yahoo finance.
    Slice time period, if he is longer that default period

    :param data: task template from scheduler queued
    """
    data['task_id'] = FETCH_DATA_FOR_PERIOD_TASK
    start = datetime.datetime.fromisoformat(data['from'])
    finish = datetime.datetime.fromisoformat(data['to'])
    date_difference = (finish - start).days
    if date_difference > DEFAULT_PERIOD:
        count_whole_moths = date_difference // DEFAULT_PERIOD
        remainder = date_difference - (count_whole_moths * DEFAULT_PERIOD)
        for _ in range(count_whole_moths):
            data['from'] = start.isoformat()
            data['to'] = (start + datetime.timedelta(days=DEFAULT_PERIOD)).isoformat()
            worker_publish_task(json.dumps(data))
            start += datetime.timedelta(days=DEFAULT_PERIOD)
        data['from'] = start.isoformat()
        data['to'] = (start + datetime.timedelta(days=remainder)).isoformat()
        logger.info(f'Send task {data} to workers')
        worker_publish_task(json.dumps(data))
    data['from'] = start.isoformat()
    data['to'] = finish.isoformat()
    logger.info(f'Send task {data} to workers')
    worker_publish_task(json.dumps(data))






def scheduler_function(ch, method, properties, body):  # pylint: disable=C0103,  W0613
    dict_body = json.loads(body)
    logger.info(f'Task {dict_body} was received')
    if dict_body['task_id'] == FETCH_NEW_STOCK_TASK:
        fetch_new_stock(dict_body)
    elif dict_body['task_id'] == FETCH_HISTORICAL_DATA_TASK:
        fetch_historical_data(dict_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def updating_stocks():
    """
    Send new data for updating stocks to queue every 15 min

    """
    while True:
        logger.info('Updating stocks data was starter')
        all_stocks_in_use = get_all_stocks_in_use()

        if all_stocks_in_use:
            for stock in all_stocks_in_use:
                last_record = get_stocks_data_last_record(stock_get_id(stock))
                worker_publish_task(
                    Task(
                        task_id=FETCH_DATA_FOR_PERIOD_TASK,
                        stock_name=stock,
                        date_from=last_record,
                        date_to=datetime.datetime.now()
                    ).data_for_period_task()
                )
        logger.info('Updating stocks data was complete')
        time.sleep(UPDATING_TIME)


def check_new_stocks_rmq():
    """
    Start check_new_stocks function in loop
    """
    while True:
        check_new_stocks()
        time.sleep(UPDATING_DAILY_TIME)


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=connect_rmq)
    p2 = multiprocessing.Process(target=updating_stocks)
    p3 = multiprocessing.Process(target=check_new_stocks_rmq)
    p1.start()
    logger.info('p1 was started')
    time.sleep(5)
    p2.start()
    logger.info('p2 was started')
    time.sleep(5)
    p3.start()
    logger.info('p3 was started')
    time.sleep(5)

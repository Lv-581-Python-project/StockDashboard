import json

from scheduler_queue import scheduler_publish_task


def send_get_stock_names_function_to_scheduler():
    queue = 'get_stock_names_queue'
    parameter = 'parameter'
    body = json.dumps({"queue": queue,
                       "parameter": parameter})
    scheduler_publish_task(body)


def send_get_stock_data_function_to_scheduler():
    queue = 'get_stock_data_queue'
    parameter1 = 'parameter1'
    parameter2 = 'parameter2'
    body = json.dumps({"queue": queue,
                       "parameter1": parameter1,
                       "parameter2": parameter2})
    scheduler_publish_task(body)


send_get_stock_names_function_to_scheduler()
send_get_stock_data_function_to_scheduler()

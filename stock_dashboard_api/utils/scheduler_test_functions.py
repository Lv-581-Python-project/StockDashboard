import json

from scheduler_queue import publish_task


def send_get_names_function_to_scheduler():
    queue = 'get_stock_names_queue'
    parameter = 'parameter'
    body = json.dumps({"queue": queue,
                       "parameter": parameter})
    publish_task(body)


def send_get_data_function_to_scheduler():
    queue = 'get_stock_data_queue'
    parameter1 = 'parameter1'
    parameter2 = 'parameter2'
    body = json.dumps({"queue": queue,
                       "parameter1": parameter1,
                       "parameter2": parameter2})
    publish_task(body)


send_get_names_function_to_scheduler()
send_get_data_function_to_scheduler()

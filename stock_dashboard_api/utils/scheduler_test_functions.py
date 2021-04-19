import json

from scheduler_queue import publish_task


def send_worker1_function_to_scheduler():
    queue = 'queue1'
    parameter = 'queue1_parameter'
    body = json.dumps({"queue": queue,
                       "parameter": parameter})
    publish_task(body)


def send_worker2_function_to_scheduler():
    queue = 'queue2'
    parameter1 = 'queue2_parameter1'
    parameter2 = 'queue2_parameter2'
    body = json.dumps({"queue": queue,
                       "parameter1": parameter1,
                       "parameter2": parameter2})
    publish_task(body)


send_worker1_function_to_scheduler()
send_worker2_function_to_scheduler()

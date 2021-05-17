import json

from constants import FETCH_HISTORICAL_DATA,\
    FETCH_DATA_FOR_PERIOD, FETCH_NEW_STOCK


class Task:
    """
    Class for representation of different tasks
    """
    STOCK_NAME = 0
    FROM = 1
    TO = 2

    def __init__(self, task_id):
        """
        Initialization of task id
        :param task_id: number of task
        """
        self.task_id = task_id

    def form_task(self, *params):
        """
        Form a body for a task depend on task id
        :param params: Params for worker
        :return: json with parameters
        """
        if self.task_id == FETCH_DATA_FOR_PERIOD:
            body = json.dumps({"task_id": FETCH_DATA_FOR_PERIOD,
                               "stock_name": params[Task.STOCK_NAME],
                               "from": params[Task.FROM],
                               "to": params[Task.TO]})
            return body
        elif self.task_id == FETCH_NEW_STOCK:
            body = json.dumps({"task_id": FETCH_NEW_STOCK,
                               "stock_name": params[Task.STOCK_NAME]})
            return body
        elif self.task_id == FETCH_HISTORICAL_DATA:
            body = json.dumps({"task_id": FETCH_HISTORICAL_DATA,
                               "stock_name": params[Task.STOCK_NAME],
                               "from": params[Task.FROM],
                               "to": params[Task.TO]})
            return body

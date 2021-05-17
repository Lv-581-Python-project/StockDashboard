import json

from constants import FETCH_HISTORICAL_DATA_TASK,\
    FETCH_DATA_FOR_PERIOD_TASK, FETCH_NEW_STOCK_TASK


class Task:
    """
    Class for representation of different tasks
    """
    STOCK_NAME_INDEX = 0
    FROM_INDEX = 1
    TO_INDEX = 2

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
        if self.task_id == FETCH_DATA_FOR_PERIOD_TASK:
            body = json.dumps({"task_id": FETCH_DATA_FOR_PERIOD_TASK,
                               "stock_name": params[Task.STOCK_NAME_INDEX],
                               "from": params[Task.FROM_INDEX],
                               "to": params[Task.TO_INDEX]})
            return body
        elif self.task_id == FETCH_NEW_STOCK_TASK:
            body = json.dumps({"task_id": FETCH_NEW_STOCK_TASK,
                               "stock_name": params[Task.STOCK_NAME_INDEX]})
            return body
        elif self.task_id == FETCH_HISTORICAL_DATA_TASK:
            body = json.dumps({"task_id": FETCH_HISTORICAL_DATA_TASK,
                               "stock_name": params[Task.STOCK_NAME_INDEX],
                               "from": params[Task.FROM_INDEX],
                               "to": params[Task.TO_INDEX]})
            return body

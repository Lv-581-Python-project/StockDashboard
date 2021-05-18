import json

from workers.utils.constants import (FETCH_HISTORICAL_DATA_TASK,
                                     FETCH_DATA_FOR_PERIOD_TASK,
                                     FETCH_NEW_STOCK_TASK)
from workers.utils.logger import workers_logger as logger


class Task:
    MESSAGE = "Wrong type of task for worker"
    """
    Class for representation of different tasks
    """
    def __init__(self, task_id, stock_name, date_from=None, date_to=None):
        """
        Initialization of task id and params
        :param task_id: number of task
        :param stock_name: name of stock
        :param date_from: date from
        :param date_to: date to
        """
        self.task_id = task_id
        self.stock_name = stock_name
        self.date_from = date_from
        self.date_to = date_to

    def new_stock_task(self):
        """
        Task for get new stock
        :return: body for task
        """
        if self.task_id != FETCH_NEW_STOCK_TASK:
            logger.info(Task.MESSAGE)
            raise Exception(Task.MESSAGE)
        body = json.dumps({"task_id": self.task_id,
                          "stock_name": self.stock_name})
        return body

    def historical_data_task(self):
        """
        Task for get fetch historical data
        :return: body for task
        """
        if self.task_id != FETCH_HISTORICAL_DATA_TASK:
            logger.info(Task.MESSAGE)
            raise Exception(Task.MESSAGE)
        body = json.dumps({"task_id": self.task_id,
                           "stock_name": self.stock_name,
                           "from": self.date_from,
                           "to": self.date_to})
        return body

    def data_for_period_task(self):
        """
        Task for get new data for some period
        :return: body for task
        """
        if self.task_id != FETCH_DATA_FOR_PERIOD_TASK:
            logger.info(Task.MESSAGE)
            raise Exception(Task.MESSAGE)
        body = json.dumps({"task_id": self.task_id,
                           "stock_name": self.stock_name,
                           "from": self.date_from,
                           "to": self.date_to})
        return body

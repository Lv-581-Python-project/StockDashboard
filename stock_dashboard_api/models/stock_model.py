from __future__ import annotations

from datetime import datetime, timedelta

import psycopg2

from stock_dashboard_api.models.stock_data_models import StockData
from stock_dashboard_api.utils.constants import DATETIME_PATTERN
from stock_dashboard_api.utils.logger import models_logger as logger
from stock_dashboard_api.utils.pool import pool_manager


class Stock:
    """
    Model used to create, update, delete and get instance from database"
    """
    _table = 'public.stocks'

    def __init__(self, name: str, company_name: str, pk: int = None, in_use: bool = False):
        """
        :param name: short name of company stocks
        :param company_name: name of company
        :param pk: company id in database
        :param in_use: flag to show if data was used before or not
        """

        self.pk = pk  # pylint: disable=C0103
        self.name = name
        self.company_name = company_name
        self.in_use = in_use

    @classmethod
    def create(cls, name: str, company_name: str) -> Stock:
        """
        Create a new instance in database

        :param name: short name of company stocks
        :param company_name: name of company
        :return: instance
        """

        with pool_manager() as conn:
            query = f"""INSERT INTO {cls._table} (name, company_name)
                        VALUES (%(name)s, %(company_name)s)
                        RETURNING id, name, company_name, in_use;"""
            try:
                conn.cursor.execute(query, {'name': name, 'company_name': company_name})
                pk, name, company_name, in_use = conn.cursor.fetchone()  # pylint: disable=C0103
                return Stock(pk=pk, name=name, company_name=company_name, in_use=in_use)
            except (psycopg2.DataError, psycopg2.ProgrammingError):
                message = f"Could not create Stock with name={name}, company_name={company_name}"
                logger.warning(message)

    def update(self, name: str = None, company_name: str = None) -> bool:
        """
        Update an existing instance in database

        :param name:
        :param company_name:
        :return: True if update was successful and False if not
        """

        data_to_update = []
        if name is not None:
            data_to_update.append("name = %(name)s")
        if company_name is not None:
            data_to_update.append("company_name = %(company_name)s")
        query = f"""UPDATE {self._table} SET {', '.join(data_to_update)}
                WHERE id = %(pk)s RETURNING id, name, company_name, in_use; """
        with pool_manager() as conn:
            try:
                conn.cursor.execute(
                    query,
                    {'name': name, 'company_name': company_name, 'pk': self.pk, 'in_use': self.in_use})
                pk, name, company_name, in_use = conn.cursor.fetchone()  # pylint: disable=C0103, W0612
                self.name = name
                self.company_name = company_name
                return True
            except (psycopg2.DataError, psycopg2.ProgrammingError):
                return False

    @classmethod
    def delete_by_id(cls, pk: int) -> bool:  # pylint: disable=C0103
        """
        Delete instance by id in database

        :param pk: instance id in database
        :return: True if delete was successful and False if not
        """

        if not Stock.get_by_id(pk):
            return False
        with pool_manager() as conn:
            query = f"DELETE FROM {cls._table} WHERE id = %(id)s;"
            try:
                conn.cursor.execute(query, {'id': pk})
                return True
            except(psycopg2.DataError, psycopg2.ProgrammingError):
                return False

    @classmethod
    def get_by_id(cls, pk: int) -> Stock:  # pylint: disable=C0103
        """
        Get instance from database by id

        :param pk: instance id in database
        :return: instance from database
        """

        with pool_manager() as conn:
            query = f"SELECT id, name, company_name, in_use FROM {cls._table} WHERE id = %(id)s"
            try:
                conn.cursor.execute(query, {'id': pk})
                pk, name, company_name, in_use = conn.cursor.fetchone()
                return Stock(pk=pk, name=name, company_name=company_name, in_use=in_use)
            except (psycopg2.DataError, psycopg2.ProgrammingError, TypeError):
                message = f"Could not get stock by pk={pk}"
                logger.warning(message)

    @classmethod
    def get_all(cls) -> list:
        """
        Get all stocks from database
        """

        stocks = []
        with pool_manager() as conn:
            query = f"SELECT id, name, company_name, in_use FROM {cls._table};"
            try:
                conn.cursor.execute(query)
                stocks = conn.cursor.fetchall()
            except (psycopg2.DataError, psycopg2.ProgrammingError, TypeError):
                message = "Could not get stocks"
                logger.warning(message)
            stocks = [Stock(pk=pk, name=name, company_name=company_name, in_use=in_use)
                      for pk, name, company_name, in_use in stocks]
        return stocks

    @classmethod
    def get_stock_by_ids(cls, stock_ids):
        stock_ids = tuple(stock_ids)
        select_stocks_query = f"""SELECT id, name, company_name, in_use FROM {cls._table} WHERE id IN %(stock_ids)s"""
        with pool_manager() as conn:
            try:
                conn.cursor.execute(select_stocks_query, {'stock_ids': stock_ids})
                stocks = conn.cursor.fetchall()
                stocks = [Stock(pk=stock[0], name=stock[1],company_name= stock[2], in_use=stock[3]) for stock in stocks]
                return stocks
            except (psycopg2.DataError, psycopg2.ProgrammingError, TypeError):
                message = "Could not get stocks"
                logger.warning(message)

    def get_data_for_time_period(self, datetime_from: datetime, datetime_to: datetime) -> list:
        """
        Return list of stock datas for current stock in specified period of time

        :param datetime_from: start time of period to get stock data
        :param datetime_to: end time of period to get stock data
        :return: list of StockData
        """

        stock_data_for_time_period = []
        datetime_from, datetime_to = datetime_from.strftime(DATETIME_PATTERN), datetime_to.strftime(DATETIME_PATTERN)
        with pool_manager() as conn:
            query = "SELECT id, name, company_name, in_use FROM stocks_data " \
                    "WHERE stock_id = %(stock_id)s " \
                    "AND %(datetime_from)s <= created_at AND created_at < %(datetime_to)s " \
                    "ORDER BY created_at;"
            try:
                conn.cursor.execute(query, {'stock_id': self.pk,
                                            'datetime_from': datetime_from,
                                            'datetime_to': datetime_to})
                stock_data_for_time_period = conn.cursor.fetchall()
            except (psycopg2.DataError, psycopg2.ProgrammingError, TypeError):
                message = f"Could not get stock data for pk={self.pk}, datetime_from={datetime_from}, " \
                          f"datetime_to={datetime_to}"
                logger.warning(message)
            stock_data_for_time_period = [StockData(pk=pk, stock_id=stock_id, price=price, created_at=created_at)
                                          for pk, stock_id, price, created_at in stock_data_for_time_period]
        return stock_data_for_time_period

    @classmethod
    def get_data_for_last_day(cls, pk: int) -> list:
        stock_data_for_last_day = []
        datetime_now = datetime.now().strftime(DATETIME_PATTERN)
        datetime_yesterday = (datetime.now() - timedelta(days=1)).strftime(DATETIME_PATTERN)
        with pool_manager() as conn:
            query = """SELECT * FROM stocks_data
                                WHERE stock_id = %(stock_id)s
                                AND %(yesterday)s <= created_at AND created_at < %(today)s
                                ORDER BY created_at;"""
            try:
                conn.cursor.execute(query, {'stock_id': pk,
                                            'yesterday': datetime_yesterday,
                                            'today': datetime_now})
                stock_data_for_last_day = conn.cursor.fetchall()
            except (psycopg2.DataError, psycopg2.ProgrammingError, TypeError) as err:
                logger.info(f"Error! {err}")

        stock_data_for_last_day = [StockData(pk=pk, stock_id=stock_id, price=price, created_at=created_at)
                                   for pk, stock_id, price, created_at in stock_data_for_last_day]
        return stock_data_for_last_day

    def to_dict(self) -> dict:
        """
        Used to instance represent in dict format

        :return: dictionary with information about instance
        """

        return {'id': self.pk, "name": self.name, "company_name": self.company_name, "in_use": self.in_use}

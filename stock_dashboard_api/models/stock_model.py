from __future__ import annotations

from datetime import datetime, timedelta

import psycopg2

from stock_dashboard_api.models.stock_data_models import StockData
from stock_dashboard_api.utils.constants import DATETIME_PATTERN, STOCK_DATA_INTERVAL, FETCH_HISTORICAL_DATA_TASK
from stock_dashboard_api.utils.logger import models_logger as logger
from stock_dashboard_api.utils.pool import pool_manager
from stock_dashboard_api.utils.scheduler_queue import scheduler_publish_task
from stock_dashboard_api.utils.worker_task import Task


class Stock:
    """
    Model used to create, update, delete and get instance from database"
    """
    _table = 'public.stocks'

    def __init__(self, name: str, company_name: str, country: str, industry: str, sector: str, pk: int = None, in_use: bool = False):
        """
        :param name: short name of company stocks
        :param company_name: name of company
        :param country: country
        :param industry: industry
        :param sector: sector
        :param pk: company id in database
        :param in_use: flag to show if data was used before or not
        """

        self.pk = pk  # pylint: disable=C0103
        self.name = name
        self.company_name = company_name
        self.country = country
        self.industry = industry
        self.sector = sector
        self.in_use = in_use

    @classmethod
    def create(cls, name: str, company_name: str, country: str, industry: str, sector: str, in_use: bool = None) -> Stock:
        """
        Create a new instance in database

        :param name: short name of company stocks
        :param company_name: name of company
        :param country:
        :param industry:
        :param sector:
        :return: instance
        """

        with pool_manager() as conn:
            query = f"""INSERT INTO {cls._table} (name, company_name, country, industry, sector)
                        VALUES (%(name)s, %(company_name)s)
                        RETURNING id, name, company_name, country, industry, sector, in_use;"""
            try:
                conn.cursor.execute(query,
                                    {'name': name,
                                     'company_name': company_name,
                                     'country': country,
                                     'industry': industry,
                                     'sector': sector})
                pk, name, company_name, country, industry, sector, in_use = conn.cursor.fetchone()  # pylint: disable=C0103
                return Stock(pk=pk,
                             name=name,
                             company_name=company_name,
                             country=country,
                             industry=industry,
                             sector=sector,
                             in_use=in_use)
            except (psycopg2.DataError, psycopg2.ProgrammingError):
                message = f"Could not create Stock with name={name}, company_name={company_name}"
                logger.warning(message)

    def update(self, name: str = None, company_name: str = None, country: str = None, industry: str = None,
               sector: str = None, in_use: bool = None) -> bool:
        """
        Update an existing instance in database

        :param name:
        :param company_name:
        :param country:
        :param industry:
        :param sector:
        :param in_use:
        :return: True if update was successful and False if not
        """

        data_to_update = []
        if name is not None:
            data_to_update.append("name = %(name)s")
        if company_name is not None:
            data_to_update.append("company_name = %(company_name)s")
        query = f"""UPDATE {self._table} SET {', '.join(data_to_update)}
                WHERE id = %(pk)s RETURNING id, name, company_name, country, industry, sector, in_use; """
        with pool_manager() as conn:
            try:
                conn.cursor.execute(
                    query,
                    {'name': name,
                     'company_name': company_name,
                     'country': country,
                     'industry': industry,
                     'sector': sector,
                     'pk': self.pk,
                     'in_use': self.in_use})
                pk, name, company_name, country, industry, sector, in_use = conn.cursor.fetchone()  # pylint: disable=C0103, W0612
                self.name = name
                self.company_name = company_name
                self.country = country
                self.industry = industry
                self.sector = sector
                self.in_use = in_use
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
            query = f"SELECT id, name, company_name, country, industry, sector, in_use FROM {cls._table} WHERE id = %(id)s"
            try:
                conn.cursor.execute(query, {'id': pk})
                pk, name, company_name, country, industry, sector, in_use = conn.cursor.fetchone()
                return Stock(pk=pk,
                             name=name,
                             company_name=company_name,
                             country=country,
                             industry=industry,
                             sector=sector,
                             in_use=in_use)
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
            query = f"SELECT id, name, company_name, country, industry, sector, in_use FROM {cls._table};"
            try:
                conn.cursor.execute(query)
                stocks = conn.cursor.fetchall()
            except (psycopg2.DataError, psycopg2.ProgrammingError, TypeError):
                message = "Could not get stocks"
                logger.warning(message)
            stocks = [Stock(pk=pk,
                            name=name,
                            company_name=company_name,
                            country=country,
                            industry=industry,
                            sector=sector,
                            in_use=in_use)
                      for pk, name, company_name, country, industry, sector, in_use in stocks]
        return stocks

    @classmethod
    def get_stock_by_ids(cls, stock_ids):
        stock_ids = tuple(stock_ids)
        select_stocks_query = f"""SELECT id, name, company_name, country, industry, sector, in_use FROM {cls._table} 
                                  WHERE id IN %(stock_ids)s"""
        with pool_manager() as conn:
            try:
                conn.cursor.execute(select_stocks_query, {'stock_ids': stock_ids})
                stocks = conn.cursor.fetchall()
                stocks = [Stock(pk=stock[0],
                                name=stock[1],
                                company_name=stock[2],
                                country=stock[3],
                                industry=stock[4],
                                sector=stock[5],
                                in_use=stock[6])
                          for stock in stocks]
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
        datetime_from_str, datetime_to_str = datetime_from.strftime(DATETIME_PATTERN), datetime_to.strftime(
            DATETIME_PATTERN)
        with pool_manager() as conn:
            query = "SELECT id, stock_id, price, created_at FROM stocks_data " \
                    "WHERE stock_id = %(stock_id)s " \
                    "AND %(datetime_from)s <= created_at AND created_at < %(datetime_to)s " \
                    "ORDER BY created_at;"
            try:
                conn.cursor.execute(query, {'stock_id': self.pk,
                                            'datetime_from': datetime_from_str,
                                            'datetime_to': datetime_to_str})
                stock_data_for_time_period = conn.cursor.fetchall()
            except (psycopg2.DataError, psycopg2.ProgrammingError, TypeError):
                message = f"Could not get stock data for pk={self.pk}, datetime_from={datetime_from_str}, " \
                          f"datetime_to={datetime_to_str}"
                logger.warning(message)

            stock_data_for_time_period = [StockData(pk=pk, stock_id=stock_id, price=price, created_at=created_at)
                                          for pk, stock_id, price, created_at in stock_data_for_time_period]

            if Stock._are_gaps_in_data(datetime_from, datetime_to, stock_data_for_time_period):
                self._fill_gaps_in_data(datetime_from, datetime_to, stock_data_for_time_period)

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

    @classmethod
    def _are_gaps_in_data(cls, datetime_from: datetime, datetime_to: datetime, stock_data: list):
        """
        Checks if there are gaps in stock data

        :param datetime_from: datetime to start check for gaps from
        :param datetime_to: datetime to finish check for gaps from
        :param stock_data: list of StockData to check for gaps
        """

        time_period_in_minutes = datetime_to.timestamp() - datetime_from.timestamp() / 60
        expected_data_quantity = time_period_in_minutes / (60 / STOCK_DATA_INTERVAL)
        actual_data_quantity = len(stock_data)
        return actual_data_quantity != expected_data_quantity

    def _fill_gaps_in_data(self, datetime_from, datetime_to, stock_data):
        """
        Sends task to scheduler queue for filling gaps in stock data

        :param datetime_from: datetime to start filling gaps from
        :param datetime_to: datetime to finish filling gaps from
        :param stock_data: list of StockData to fill for gaps
        """

        gaps = Stock._get_gaps_in_data(datetime_from, datetime_to, stock_data)
        datetime_from_index = 0
        datetime_to_index = 1
        for gap in gaps:
            rmq_task = Task(FETCH_HISTORICAL_DATA_TASK,
                            self.name,
                            gap[datetime_from_index].isoformat(),
                            gap[datetime_to_index].isoformat())
            publish_task(rmq_task.historical_data_task())

    @classmethod
    def _get_gaps_in_data(cls, datetime_from: datetime, datetime_to: datetime, stock_data: list):
        """
        Looking for gaps in stock data

        :param datetime_from: datetime to start looking for gaps from
        :param datetime_to: datetime to finish looking for gaps from
        :param stock_data: list of StockData to look for gaps
        """

        def is_gap(_datetime_from: datetime, _datetime_to: datetime):
            return (_datetime_to.timestamp() - _datetime_from.timestamp()) / 60 > STOCK_DATA_INTERVAL

        stock_data.sort(key=lambda x: x.created_at)
        gaps = {}  # key - gap start, value - gap end. in order to gaps being unique and dont have duplicates

        if len(stock_data) == 0:
            gaps[datetime_from] = datetime_to
        else:
            if is_gap(datetime_from, stock_data[0].created_at):
                gaps[datetime_from] = stock_data[0].created_at
            for i in range(len(stock_data) - 1):
                potential_gap_start, potential_gap_end = stock_data[i].created_at, stock_data[i + 1].created_at
                if is_gap(potential_gap_start, potential_gap_end):
                    gaps[potential_gap_start] = potential_gap_end
            if is_gap(stock_data[-1].created_at, datetime_to):
                gaps[stock_data[-1].created_at] = datetime_to

        return [(_datetime_from, _datetime_to) for _datetime_from, _datetime_to in gaps.items()]

    def to_dict(self) -> dict:
        """
        Used to instance represent in dict format

        :return: dictionary with information about instance
        """

        return {'id': self.pk,
                "name": self.name,
                "company_name": self.company_name,
                "country": self.country,
                "industry": self.industry,
                "sector": self.sector,
                "in_use": self.in_use}

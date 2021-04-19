from datetime import datetime

import psycopg2

from stock_dashboard_api.utils.pool import pool_manager

DATETIME_PATTERN = "%Y-%m-%d %H:%M:%S"


class Stock:
    """
    Model used to create, update, delete and get instance from database"
    """
    _table = 'public.stocks'

    def __init__(self, name: str, company_name: str, pk: int = None) -> object:
        """
        :param name: short name of company stocks
        :param company_name: name of company
        :param pk: company id in database
        """

        self.pk = pk  # pylint: disable=C0103
        self.name = name
        self.company_name = company_name

    @classmethod
    def create(cls, name: str, company_name: str) -> object:
        """
        Create a new instance in database

        :param name: short name of company stocks
        :param company_name: name of company
        :return: instance
        """

        with pool_manager() as conn:
            query = f"""INSERT INTO {cls._table} (name, company_name)
                        VALUES (%(name)s, %(company_name)s)
                        RETURNING id, name, company_name;"""
            try:
                conn.cursor.execute(query, {'name': name, 'company_name': company_name})
                pk, name, company_name = conn.cursor.fetchone()  # pylint: disable=C0103
                return Stock(pk=pk, name=name, company_name=company_name)
            except (psycopg2.DataError, psycopg2.ProgrammingError):
                return False

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
                WHERE id = %(pk)s RETURNING id, name, company_name; """
        with pool_manager() as conn:
            try:
                conn.cursor.execute(
                    query,
                    {'name': name, 'company_name': company_name, 'pk': self.pk})
                pk, name, company_name = conn.cursor.fetchone()  # pylint: disable=C0103, W0612
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
    def get_by_id(cls, pk: int) -> object:  # pylint: disable=C0103
        """
        Get instance from database by id

        :param pk: instance id in database
        :return: instance from database
        """

        with pool_manager() as conn:
            query = f"SELECT id, name, company_name FROM {cls._table} WHERE id = %(id)s"
            try:
                conn.cursor.execute(query, {'id': pk})
                pk, name, company_name = conn.cursor.fetchone()
                return Stock(pk=pk, name=name, company_name=company_name)
            except (psycopg2.DataError, psycopg2.ProgrammingError, TypeError):
                return None

    def get_data_for_time_period(self, datetime_from: datetime, datetime_to: datetime) -> list:
        stock_data_for_time_period = []
        datetime_from, datetime_to = datetime_from.strftime(DATETIME_PATTERN), datetime_to.strftime(DATETIME_PATTERN)
        with pool_manager() as conn:
            query = "SELECT price, created_at FROM stocks_data " \
                    "WHERE stock_id = %(stock_id)s " \
                    "AND %(datetime_from)s <= created_at AND created_at <= %(datetime_to)s " \
                    "ORDER BY created_at;"
            try:
                conn.cursor.execute(query, {'stock_id': self.pk,
                                            'datetime_from': datetime_from,
                                            'datetime_to': datetime_to})
                stock_data_for_time_period = conn.cursor.fetchall()
            except (psycopg2.DataError, psycopg2.ProgrammingError, TypeError) as e:
                print(e)
                return stock_data_for_time_period
        return stock_data_for_time_period

    def to_dict(self) -> dict:
        """
        Used to instance represent in dict format

        :return: dictionary with information about instance
        """

        return {'id': self.pk, "name": self.name, "company_name": self.company_name}

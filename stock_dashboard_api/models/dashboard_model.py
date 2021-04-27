import psycopg2

from stock_dashboard_api.utils.dashboard_hash_generator import generate_dashboard_hash
from stock_dashboard_api.utils.pool import pool_manager
from stock_dashboard_api.utils.logger import views_logger as logger
from stock_dashboard_api.models.stock_model import Stock


class Dashboard:
    """
    Model used to create a Dashboard.
    """

    _table = 'public.dashboard'

    def __init__(self, dashboard_hash: str):
        self.dashboard_hash = dashboard_hash

    @classmethod
    def create(cls, stocks: list) -> object:
        """Creates a new record in Dashboard table

        :param stocks: list of stocks for specific dashboard
        :return: instance of Dashboard
        """
        stock_names = [stock["stock_name"] for stock in stocks]
        stock_names.sort()
        stock_names = " ".join(stock_names)
        dashboard_hash = generate_dashboard_hash(stock_names=stock_names)

        # Check if dashboard already exists returning it
        existing_dashboard = Dashboard.get_by_hash(dashboard_hash)
        if existing_dashboard and existing_dashboard.dashboard_hash:
            return existing_dashboard

        with pool_manager() as conn:
            dashboard_has_stocks_table = 'public.dashboard_has_stocks'

            try:
                insert_dashboard_query = f"""INSERT INTO {cls._table} (dashboard_hash)
                                        VALUES (%(dashboard_hash)s) 
                                        RETURNING dashboard_hash;"""
                conn.cursor.execute(insert_dashboard_query, {'dashboard_hash': dashboard_hash})
                dashboard_hash = conn.cursor.fetchone()

                dashboard_has_stocks_insert_data = [(stock["stock_id"], dashboard_hash) for stock in stocks]
                insert_dashboard_has_stocks_query = (f"INSERT INTO {dashboard_has_stocks_table} "
                                                     "(stock_id, dashboard_hash)"
                                                     " VALUES (%s, %s);")
                conn.cursor.executemany(insert_dashboard_has_stocks_query, dashboard_has_stocks_insert_data)
                return Dashboard(dashboard_hash=dashboard_hash)
            except (psycopg2.ProgrammingError, psycopg2.DatabaseError) as error:
                logger.info(f"Error Dashboard model create {error}")

    def update(self, dashboard_hash: str) -> bool:
        """
        Updates an existing dashboard.
        """
        if not dashboard_hash:
            return False
        with pool_manager() as conn:
            query = f"""UPDATE {self._table} SET dashboard_hash = %(dashboard_hash)s
                        WHERE dashboard_hash = %(dashboard_hash)s
                        RETURNING dashboard_hash;"""
            try:
                conn.cursor.execute(query, {'dashboard': dashboard_hash})
                dashboard_hash = conn.cursor.fetchone()
                self.dashboard_hash = dashboard_hash
                return True
            except (psycopg2.ProgrammingError, psycopg2.DatabaseError) as error:
                logger.info(f"Error Dashboard model update {error}")

    @classmethod
    def get_by_hash(cls, dashboard_hash: str):
        """Getting a dashboard by its hash from Dashboard table

        :return: instance of DashboardConfig model
        """
        with pool_manager() as conn:
            get_dashboard_id_query = f"""SELECT dashboard_hash FROM {cls._table}
                                         WHERE dashboard_hash = %(dashboard_hash)s;"""

            try:
                conn.cursor.execute(get_dashboard_id_query, {'dashboard_hash': dashboard_hash})
                dashboard_hash = conn.cursor.fetchone()
                return Dashboard(dashboard_hash=dashboard_hash)
            except (psycopg2.ProgrammingError, psycopg2.DatabaseError, TypeError) as error:
                logger.info(f"Error Dashboard model get_by_hash {error}")

    def get_stocks(self):
        dashboard_has_stocks_table = 'public.dashboard_has_stocks'
        stocks_table = 'public.stocks'
        with pool_manager() as conn:
            get_stocks_id_query = f"""SELECT {dashboard_has_stocks_table}.stock_id,{stocks_table}.name,
                                             {stocks_table}.company_name,{stocks_table}.in_use
                                      FROM {dashboard_has_stocks_table} INNER JOIN {stocks_table} 
                                      ON {dashboard_has_stocks_table}.stock_id = {stocks_table}.id
                                      WHERE {dashboard_has_stocks_table}.dashboard_hash = %(dashboard_hash)s;"""
            try:
                conn.cursor.execute(get_stocks_id_query, {'dashboard_hash': self.dashboard_hash})
                list_of_stocks = conn.cursor.fetchall()
                list_of_stocks = [Stock(pk=stock[0], name=stock[1], company_name=stock[2], in_use=stock[3]).to_dict()
                                  for stock in list_of_stocks]
                return list_of_stocks
            except (psycopg2.ProgrammingError, psycopg2.DatabaseError, TypeError) as error:
                logger.info(f"Error Dashboard model get_stocks {error}")

    @classmethod
    def delete_by_hash(cls, dashboard_hash: str) -> bool:
        """
        Deletes a Dashboard instance by its dashboard_hash.
        """

        if not Dashboard.get_by_hash(dashboard_hash):
            return False

        with pool_manager() as conn:
            query = f"DELETE FROM {cls._table} WHERE dashboard_hash = %(dashboard_hash)s;"
            try:
                conn.cursor.execute(query, {'dashboard_hash': dashboard_hash})
                return True
            except(psycopg2.DataError, psycopg2.ProgrammingError) as error:
                logger.info(f"Error Dashboard model delete_by_hash {error}")

    def to_dict(self) -> dict:
        """
        Used to represent the instance in dictionary format
        :return: dictionary with the information about instance
        """
        return {'dashboard_hash': self.dashboard_hash}

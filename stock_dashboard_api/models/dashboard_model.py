import psycopg2

from stock_dashboard_api.utils.dashboard_hash_generator import generate_uuid
from stock_dashboard_api.utils.pool import pool_manager


class Dashboard:
    """
    Model used to create a Dashboard.
    """

    _table = 'public.dashboard'

    def __init__(self, config_hash: str, pk=None):  # pylint: disable=C0103,  W0613
        self.pk = pk  # pylint: disable=C0103,  W0613
        self.config_hash = config_hash

    @classmethod
    def create(cls, config_hash=None, stocks=None) -> object:
        """Creates a new record in Dashboard table

        :param config_hash: specific config hash for record
        :param stocks: list of stocks for specific dashboard
        :return: instance of Dashboard
        """

        if not config_hash:
            all_config_hashes = Dashboard.get_all_hashes()
            config_hash = generate_uuid(all_config_hashes)
        with pool_manager() as conn:
            dashboard_has_stocks_table = 'public.dashboard_has_stocks'
            insert_dashboard_query = f"""INSERT INTO {cls._table} (config_hash)
                        VALUES (%(config_hash)s)
                        RETURNING id, config_hash;"""
            try:
                conn.cursor.execute(insert_dashboard_query, {'config_hash': config_hash})
                pk, config_hash = conn.cursor.fetchone()  # pylint: disable=C0103,  W0613
                if stocks:
                    stocks = [(stock["stock_id"], pk, stock["datetime_from"], stock["datetime_to"]) for stock in stocks]
                    insert_dashboard_has_stocks_query = (f"INSERT INTO {dashboard_has_stocks_table} "
                                                         "(stock_id, dashboard_id, datetime_from, datetime_to)"
                                                         " VALUES (%s, %s, %s, %s);")
                    conn.cursor.executemany(insert_dashboard_has_stocks_query, stocks)
            except (psycopg2.ProgrammingError, psycopg2.DatabaseError) as err:
                return False
            return Dashboard(pk=pk, config_hash=config_hash)

    def update(self, config_hash: str) -> bool:
        """
        Updates an existing dashboard.
        """
        if not config_hash:
            return False
        with pool_manager() as conn:
            query = f"""UPDATE {self._table} SET config_hash = %(config_hash)s WHERE id = %(pk)s
                        RETURNING id, config_hash;"""
            try:
                conn.cursor.execute(query, {'config_hash': config_hash, 'pk': self.pk})
                pk, config_hash = conn.cursor.fetchone()  # pylint: disable=C0103,  W0613, W0612
                self.config_hash = config_hash
            except (psycopg2.ProgrammingError, psycopg2.DatabaseError) as err:
                return False
        return True

    @classmethod
    def get_by_id(cls, pk: int) -> object:  # pylint: disable=C0103,  W0613
        """
        Returns a Dashboard instance by its id.
        :return: instance of DashboardConfig model
        """

        with pool_manager() as conn:
            query = f"SELECT * FROM {cls._table} WHERE id = %(id)s;"
            try:
                conn.cursor.execute(query, {'id': pk})
                pk, config_hash = conn.cursor.fetchone()
                return Dashboard(pk=pk, config_hash=config_hash)
            except (psycopg2.ProgrammingError, psycopg2.DatabaseError, TypeError) as err:
                return None

    @classmethod
    def get_by_hash(cls, config_hash: str):
        """Getting a dashboard by its hash from Dashboard table

        :return: instance of DashboardConfig model
        """
        with pool_manager() as conn:
            get_dashboard_id_query = f"SELECT id FROM {cls._table} WHERE config_hash = %(config_hash)s;"

            try:
                conn.cursor.execute(get_dashboard_id_query, {'config_hash': config_hash})
                pk = conn.cursor.fetchone()[0]
                return Dashboard(pk=pk, config_hash=config_hash)
            except (psycopg2.ProgrammingError, psycopg2.DatabaseError, TypeError):
                return None
            
    @classmethod
    def get_all_hashes(cls) -> list:
        """
        Getting all config hashes from Dashboard table
        :return: list of dashboard config hashes
        """
        with pool_manager() as conn:
            query = f"""SELECT config_hash FROM {cls._table};"""
            try:
                conn.cursor.execute(query)

                all_config_hashes = conn.cursor.fetchall()
                all_config_hashes = [config_hash[0] for config_hash in all_config_hashes]
                return all_config_hashes
            except (psycopg2.ProgrammingError, psycopg2.DatabaseError) as err:
                return None

    def get_stocks(self):
        dashboard_has_stocks_table = 'public.dashboard_has_stocks'
        with pool_manager() as conn:
            get_stocks_id_query = f"""SELECT stock_id
                                      FROM {dashboard_has_stocks_table}
                                      WHERE {dashboard_has_stocks_table}.dashboard_id=%(id)s;"""
            try:
                conn.cursor.execute(get_stocks_id_query, {'id': self.pk})
                list_of_stocks = conn.cursor.fetchall()
                list_of_stocks = [stock[0] for stock in list_of_stocks]
                return list_of_stocks
            except (psycopg2.ProgrammingError, psycopg2.DatabaseError, TypeError) as err:
                return None

    @classmethod
    def delete_by_id(cls, pk: int) -> bool:  # pylint: disable=C0103,  W0613
        """
        Deletes a dashboard_config instance by its id.
        """

        if not Dashboard.get_by_id(pk):
            return False

        with pool_manager() as conn:
            query = f"DELETE FROM {cls._table} WHERE id = %(id)s;"
            try:
                conn.cursor.execute(query, {'id': pk})
                return True
            except(psycopg2.DataError, psycopg2.ProgrammingError):
                return False

    def to_dict(self) -> dict:
        """
        Used to represent the instance in dictionary format
        :return: dictionary with the information about instance
        """
        return {'pk': self.pk,
                'config_hash': self.config_hash}

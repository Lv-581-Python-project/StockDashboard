import psycopg2

from stock_dashboard_api.utils.pool import pool_manager


class DashboardConfig:
    """
    Model used to create a dashboard_config.
    """

    _table = 'public.dashboard_config'

    def __init__(self, config_hash: str, pk=None):  # pylint: disable=C0103,  W0613
        self.pk = pk  # pylint: disable=C0103,  W0613
        self.config_hash = config_hash

    @classmethod
    def create(cls, config_hash: str) -> object:
        """
        Creates a new dashboard_config.
        :return: instance of DashboardConfig
        """
        with pool_manager() as conn:
            query = f"""INSERT INTO {cls._table} (config_hash)
                        VALUES (%(config_hash)s)
                        RETURNING id, config_hash;"""
            try:
                conn.cursor.execute(query, {'config_hash': config_hash})
                pk, config_hash = conn.cursor.fetchone()  # pylint: disable=C0103,  W0613
            except (psycopg2.ProgrammingError, psycopg2.DatabaseError) as err:
                return False
            return DashboardConfig(pk=pk, config_hash=config_hash)

    def update(self, config_hash: str) -> bool:
        """
        Updates an existing dashboard_config.
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
        Returns a dashboard_config instance by its id.
        :return: instance of DashboardConfig model
        """

        with pool_manager() as conn:
            query = f"SELECT * FROM {cls._table} WHERE id = %(id)s"
            try:
                conn.cursor.execute(query, {'id': pk})
                pk, config_hash = conn.cursor.fetchone()
                return DashboardConfig(pk=pk, config_hash=config_hash)
            except (psycopg2.ProgrammingError, psycopg2.DatabaseError, TypeError) as err:
                return None

    @classmethod
    def delete_by_id(cls, pk: int) -> bool:  # pylint: disable=C0103,  W0613
        """
        Deletes a dashboard_config instance by its id.
        """

        if not DashboardConfig.get_by_id(pk):
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

from stock_dashboard_api.utils import pool as db
import psycopg2


class DashboardConfig:
    """
    Model used to create a dashboard_config.
    """
    _table = 'public.dashboard_config'

    def __init__(self, config_hash: str, pk=None):
        self.pk = pk
        self.config_hash = config_hash

    @classmethod
    def create(cls, config_hash: str):
        """
        Creates a new dashboard_config.
        """
        with db.Connection() as conn:
            query = f"""INSERT INTO {cls._table} (config_hash)
                        VALUES (%(config_hash)s)
                        RETURNING id, config_hash;"""
            conn.cursor.execute(query, {'config_hash': config_hash})
            pk, config_hash = conn.cursor.fetchone()
            return DashboardConfig(pk=pk, config_hash=config_hash)

    def update(self, config_hash):
        """
        Updates an existing dashboard_config.
        """
        if config_hash:
            with db.Connection() as conn:
                query = f"""UPDATE {self._table} SET config_hash = %(config_hash)s WHERE id = %(pk)s
                            RETURNING id, config_hash;"""
                try:
                    conn.cursor.execute(query, {'config_hash': config_hash, 'pk': self.pk})
                    pk, config_hash = conn.cursor.fetchone()
                    self.config_hash = config_hash
                except psycopg2.ProgrammingError:
                    pass

    @classmethod
    def get_by_id(cls, pk: int):
        """
        Returns a dashboard_config instance by its id.
        """
        with db.Connection() as conn:
            query = f"SELECT * FROM {cls._table} WHERE ID = %(pk)s;"
            try:
                conn.cursor.execute(query, {'pk': pk})
                pk, config_hash = conn.cursor.fetchone()
            except psycopg2.ProgrammingError:
                return None
            return DashboardConfig(pk=pk, config_hash=config_hash)

    @classmethod
    def delete_by_id(cls, pk):
        """
        Deletes a dashboard_config instance by its id.
        """
        with db.Connection() as conn:
            query = f"DELETE FROM {cls._table} WHERE id = %(pk)s;"
            conn.cursor.execute(query, {'pk': pk})

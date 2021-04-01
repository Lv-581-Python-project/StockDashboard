from stock_dashboard_api.utils import pool as db


class DashboardConfig:
    _table = 'public.dashboard_config'

    def __init__(self, config_hash, pk=None):
        self.pk = pk
        self.config_hash = config_hash

    @classmethod
    def create(cls, config_hash):
        with db.Connection() as conn:
            query = f"""INSERT INTO {cls._table} (config_hash)
                        VALUES (%(config_hash)s)
                        RETURNING id, config_hash;"""
            conn.cursor.execute(query, {'config_hash': config_hash})
            pk, config_hash = conn.cursor.fetchone()
            return DashboardConfig(pk=pk, config_hash=config_hash)

    def update(self, config_hash=None):
        if config_hash:
            with db.Connection() as conn:
                query = f"""UPDATE {self._table} SET config_hash = %(config_hash)s WHERE id = %(pk)s
                            RETURNING id, config_hash;"""
                conn.cursor.execute(query, {'config_hash': config_hash, 'pk': self.pk})
                return self

    @classmethod
    def get_by_id(cls, pk):
        with db.Connection() as conn:
            query = f"SELECT * FROM {cls._table} WHERE ID = %(pk)s;"
            conn.cursor.execute(query, {'pk': pk})
            pk, config_hash = conn.cursor.fetchone()
            return DashboardConfig(pk=pk, config_hash=config_hash)

    @classmethod
    def delete_by_id(cls, pk):
        with db.Connection() as conn:
            query = f"DELETE FROM {cls._table} WHERE id = %(pk)s;"
            conn.cursor.execute(query, {'pk': pk})

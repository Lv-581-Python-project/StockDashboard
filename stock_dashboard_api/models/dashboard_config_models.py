from stock_dashboard_api.utils import pool as db


class DashboardConfig:
    __table = 'public.dashboard_config'

    def __init__(self, config_hash, pk=None):
        self.pk = pk
        self.config_hash = config_hash

    @classmethod
    def create(cls, config_hash):
        with db.Connection() as conn:
            cursor = conn.cursor()
            query = f"""INSERT INTO {cls.__table} (config_hash)
                        "VALUES ('{config_hash}');
                        "RETURNING id, config_hash;"""
            cursor.execute(query)
            pk, config_hash = cursor.fetchone()
            conn.commit()
            cursor.close()
            return DashboardConfig(pk=pk, config_hash=config_hash)

    def update(self, config_hash=None):
        if config_hash:
            with db.Connection() as conn:
                cursor = conn.cursor()
                query = f"""UPDATE {self.__table} SET config_hash = {config_hash} WHERE id = '{self.pk};'
                            "RETURNING id, config_hash;"""
                cursor.execute(query)
                conn.commit()
                cursor.close()

    @classmethod
    def get_by_id(cls, pk):
        with db.Connection() as conn:
            cursor = conn.cursor()
            query = f"SELECT * FROM {cls.__table} WHERE ID = {pk};"
            cursor.execute(query)
            _pk, _config_hash = cursor.fetchone()
            cursor.close()
            return DashboardConfig(pk=_pk, config_hash=_config_hash)

    @classmethod
    def delete_by_id(cls, pk):
        with db.Connection() as conn:
            cursor = conn.cursor()
            query = f"DELETE FROM {cls.__table} WHERE id = {pk};"
            cursor.execute(query)
            conn.commit()
            cursor.close()

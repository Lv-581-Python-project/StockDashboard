import psycopg2
import uuid

from stock_dashboard_api.utils.pool import pool_manager


def generate_uuid():
    is_unique = False
    config_hash = ""
    while not is_unique:
        config_hash = str(uuid.uuid4())[:8]
        is_unique = check_if_unique(config_hash)
        print(config_hash)
    return config_hash


def check_if_unique(config_hash):
    _table = 'public.dashboard'
    with pool_manager() as conn:
        query = f"""SELECT id FROM {_table} 
                    WHERE config_hash=%(config_hash)s"""
        try:
            conn.cursor.execute(query, {'config_hash': config_hash})
            dashboard_id = conn.cursor.fetchone()  # pylint: disable=C0103,  W0613
            if dashboard_id:
                return False
            else:
                return True
        except (psycopg2.ProgrammingError, psycopg2.DatabaseError) as err:
            print(err)
            return False

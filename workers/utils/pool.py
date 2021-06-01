import os
import time
from psycopg2.pool import PoolError, SimpleConnectionPool

from .logger import pool_logger as logger

POOL_DELAY = os.getenv('POOL_DELAY')
TRAILS = 10


class Connection:
    """Class is used to create database connection pool"""
    connection_pool = None

    def __init__(self):
        if not Connection.connection_pool:
            Connection.connection_pool = SimpleConnectionPool(
                int(os.getenv('MINCONN')),
                int(os.getenv('MAXCONN')),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                host=os.getenv('POSTGRES_HOST'),
                port=os.getenv('POSTGRES_PORT'),
                database=os.getenv('POSTGRES_DB'))

        logger.info('Connection pool was created')
        self.conn = None
        self.cursor = None

    def __enter__(self):
        for _ in range(TRAILS):
            try:
                self.conn = Connection.connection_pool.getconn()
                self.conn.autocommit = False
                self.cursor = self.conn.cursor()
                return self

            except PoolError:
                logger.info('Pool doesn\'t have available connection. Please wait')
                time.sleep(int(POOL_DELAY))
        raise PoolError('Can\'t get a connection.')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            logger.error('Unexpected error. %s Rollback all changes', exc_val)
            self.conn.rollback()
            self.cursor.close()
            Connection.connection_pool.putconn(self.conn)
        self.conn.commit()
        self.cursor.close()
        Connection.connection_pool.putconn(self.conn)


def pool_manager():
    return pool_instance


pool_instance = Connection()

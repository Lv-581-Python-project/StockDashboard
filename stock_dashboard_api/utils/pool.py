import logging
import os
import time
from logging.config import fileConfig

from psycopg2.pool import PoolError, SimpleConnectionPool

POOL_DELAY = os.getenv('POOL_DELAY')
LOGGING_CONF = os.getenv('LOGGING_CONF')
print(LOGGING_CONF)
print(os.getcwd())
for k,v in os.environ.items():
    print(k,v)
fileConfig(LOGGING_CONF, disable_existing_loggers=True)
logger = logging.getLogger('pool')


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
        logger.info('Get connection from pool %s', id(self.conn))
        for _ in range(10):
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
        logger.info('All changes was commited')
        self.conn.commit()
        self.cursor.close()
        Connection.connection_pool.putconn(self.conn)
        logger.info('Put connection to pool %s', id(self.conn))


def pool_manager():
    return pool_instance


pool_instance = Connection()

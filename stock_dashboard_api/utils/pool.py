import logging
import os
import time
from logging.config import fileConfig
from pathlib import Path

from psycopg2.pool import PoolError, SimpleConnectionPool

POOL_DELAY = os.getenv('POOL_DELAY')

fileConfig((Path.cwd().parent / 'logging.conf'), disable_existing_loggers=True)
logger = logging.getLogger('pool')


class Connection:
    connection_pool = None

    def __init__(self):
        if not Connection.connection_pool:
            Connection.connection_pool = SimpleConnectionPool(int(os.getenv('MINCONN')),
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
        logger.info(f'Get connection from pool {id(self.conn)}')
        try:
            self.conn = Connection.connection_pool.getconn()
            self.conn.autocommit = False
            self.cursor = self.conn.cursor()
            return self

        except PoolError:
            logger.info('Pool doesn\'t have available connection. Please wait')
            time.sleep(int(POOL_DELAY))

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            logger.error(f'Unexpected error.{exc_val}. Rollback all changes')
            self.conn.rollback()
            self.cursor.close()
            Connection.connection_pool.putconn(self.conn)
        else:
            logger.info('All changes was commited')
            self.conn.commit()
            self.cursor.close()
            Connection.connection_pool.putconn(self.conn)
            logger.info(f'Put connection to pool {id(self.conn)}')

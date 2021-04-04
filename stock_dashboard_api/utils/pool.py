import logging
import os
import time
from logging.config import fileConfig

from psycopg2.pool import PoolError, SimpleConnectionPool


POOL_DELAY = os.getenv('POOL_DELAY')
LOGGING_CONF = os.getenv('LOGGING_CONF')

fileConfig(LOGGING_CONF, disable_existing_loggers=True)
logger = logging.getLogger('pool')


class Connection:
    connection_pool = None

    def __init__(self):
        if not Connection.connection_pool:
            Connection.connection_pool = SimpleConnectionPool(os.environ.get('MINCONN'),
                                                              os.environ.get('MAXCONN'),
                                                              user=os.environ.get('POSTGRES_USER'),
                                                              password=os.environ.get('POSTGRES_PASSWORD'),
                                                              host=os.environ.get('POSTGRES_HOST'),
                                                              port=os.environ.get('POSTGRES_PORT'),
                                                              database=os.environ.get('POSTGRES_DB'))

        logger.info('Connection pool was created')
        self.conn = None
        self.cursor = None

    def __enter__(self):
        logger.info('Get connection from pool {}'.format(id(self.conn)))
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
            logger.error('Unexpected error.{}. Rollback all changes'.format(exc_val))
            self.conn.rollback()
            self.cursor.close()
            Connection.connection_pool.putconn(self.conn)
        else:
            logger.info('All changes was commited')
            self.conn.commit()
            self.cursor.close()
            Connection.connection_pool.putconn(self.conn)
            logger.info('Put connection to pool {}'.format(id(self.conn)))

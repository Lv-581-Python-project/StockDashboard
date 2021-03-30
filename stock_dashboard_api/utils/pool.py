import logging
import os
import time
from logging.config import fileConfig

from dotenv import load_dotenv
from psycopg2.pool import PoolError, SimpleConnectionPool

project_folder = os.getcwd()
load_dotenv(os.path.join(project_folder, '../.env'))

POOL_DELAY = os.getenv('POOL_DELAY')

fileConfig(fname=(os.path.join(project_folder, '../_log.conf')), disable_existing_loggers=False)
logger = logging.getLogger('pool')


class Connection:
    connection_pool = None

    def __init__(self):
        if not Connection.connection_pool:
            Connection.connection_pool = SimpleConnectionPool(os.getenv('MINCONN'),
                                                              os.getenv('MAXCONN'),
                                                              user=os.getenv('POSTGRES_USER'),
                                                              password=os.getenv('POSTGRES_PASSWORD'),
                                                              host=os.getenv('POSTGRES_HOST'),
                                                              port=os.getenv('POSTGRES_PORT'),
                                                              database=os.getenv('POSTGRES_DB'))

        logger.info('Connection pool was created')
        self.conn = Connection.connection_pool.getconn()

    def __enter__(self):
        logger.info(f'Get connection from pool {id(self.conn)}')
        try:
            return self.conn

        except PoolError:
            logger.info('Pool doesn\'t have available connection. Please wait')
            time.sleep(int(POOL_DELAY))

    def __exit__(self, exc_type, exc_val, exc_tb):
        Connection.connection_pool.putconn(self.conn)
        logger.info(f'Put connection to pool {id(self.conn)}')

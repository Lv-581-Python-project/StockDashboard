import logging
from logging.config import fileConfig
import time
from psycopg2.pool import PoolError, SimpleConnectionPool
import os
from dotenv import load_dotenv

project_folder = os.getcwd()
load_dotenv(os.path.join(project_folder, '../.env'))


POOL_DELAY = os.getenv('POOL_DELAY')

fileConfig(fname=(os.path.join(project_folder, '../_log.conf')), disable_existing_loggers=False)
logger = logging.getLogger('pool')


#logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class Connection:
    connection_pool = None
    def __init__(self):
        if not Connection.connection_pool:
            Connection.connection_pool = SimpleConnectionPool(os.getenv('MINCONN'), os.getenv('MAXCONN'),
                                                              user=os.getenv('USERS'), password=os.getenv('PASSWORD'),
                                                              host=os.getenv('HOST'), port=os.getenv('PORT'),
                                                              database=os.getenv('DATABASE'))

        logger.info('Connection pool was created')
        self.conn = Connection.connection_pool.getconn()

    def __enter__(self):
        try:
            logger.info(f'Get connection from pool {id(self.conn)}')
            return self.conn

        except PoolError:
            logger.info('Pool doesn\'t have available connection. Please wait')
            time.sleep(int(POOL_DELAY))

    def __exit__(self, exc_type, exc_val, exc_tb):
        Connection.connection_pool.putconn(self.conn)
        logger.info(f'Put connection to pool {id(self.conn)}')




import logging
import time

from psycopg2.pool import PoolError, SimpleConnectionPool

pool_delay = 0.1
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

connection_pool = SimpleConnectionPool(1, 20,
                                       user="postgres",
                                       password="postgres",
                                       host="localhost",
                                       port="5432",
                                       database="postgres")

logging.info('Connection pool was created')


class Connection:
    def __init__(self, obj):
        self.obj = obj
        self.conn = self.obj.getconn()

    def __enter__(self):
        try:
            logging.info(f'Get connection from pool {id(self.conn)}')
            return self.conn

        except PoolError:
            logging.info('Pool doesn\'t have available connection. Please wait')
            time.sleep(pool_delay)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.obj.putconn(self.conn)
        logging.info(f'Put connection to pool {id(self.conn)}')


def pool_manager():
    return Connection(connection_pool)

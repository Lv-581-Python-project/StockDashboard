from stock_dashboard_api.utils.pool import pool_manager
from datetime import datetime
from psycopg2 import DataError, ProgrammingError


class StockData:
    """
    Model used to create a StockData instance.
    """
    _table = "public.stocks_data"

    def __init__(self, stock_id: int, price: float, create_at: datetime, pk=None):
        """
        :param stock_id: Stock id
        :param price: StockData price
        :param create_at: StockData creation date, time
        :param pk: StockData id
        """
        self.pk = pk
        self.stock_id = stock_id
        self.price = price
        self.create_at = create_at

    @classmethod
    def create(cls, stock_id: int, price: float, create_at: datetime):
        """
        Create new stock data
        :param stock_id: Stock id
        :param price: StockData price
        :param create_at: StockData creation date, time
        :return: StockData instance
        """
        with pool_manager() as conn:
            query = f"""INSERT INTO {cls._table} (stock_id, price, create_at)
                        VALUES (%(stock_id)s, %(price)s, %(create_at)s)
                        RETURNING id, stock_id, price, create_at;"""
            try:
                conn.cursor.execute(query, {'stock_id': stock_id,
                                            'price': price,
                                            'create_at': create_at.strftime("%Y-%m-%d %H:%M:%S")})
                pk, stock_id, price, create_at = conn.cursor.fetchone()
                return StockData(pk=pk, stock_id=stock_id, price=price, create_at=create_at)
            except(DataError, ProgrammingError):
                return None

    def update(self, price=None, create_at=None):
        """
        Changes values of the stock data to the given.
        :param price: StockData price
        :param create_at: StockData creation date, time
        :return: updated StockData instance
        """
        data_to_update = []
        if price is not None:
            data_to_update.append("price = %(price)s")
        if create_at is not None:
            data_to_update.append("create_at = %(create_at)s")
        query = f"""UPDATE {self._table} SET {', '.join(data_to_update)}
                    WHERE id = %(id)s 
                    RETURNING id, stock_id, price, create_at;"""
        with pool_manager() as conn:
            try:
                conn.cursor.execute(query, {'price': price,
                                            'create_at': create_at.strftime("%Y-%m-%d %H:%M:%S"),
                                            'id': self.pk})
                contents = conn.cursor.fetchone()
                price = contents[2]
                create_at = contents[3]
                self.price = price
                self.create_at = create_at
                return True
            except(DataError, ProgrammingError):
                return False

    @classmethod
    def get_by_id(cls, pk: int):
        """
        Get stock data with given pk.
        :param pk: StockData id
        :return: StockData instance with given pk
        """
        with pool_manager() as conn:
            query = f"SELECT * FROM {cls._table} WHERE id = %(id)s"
            try:
                conn.cursor.execute(query, {'id': pk})
                pk, stock_id, price, create_at = conn.cursor.fetchone()
                return StockData(pk=pk, stock_id=stock_id, price=price, create_at=create_at)
            except(DataError, ProgrammingError):
                return None

    @classmethod
    def delete_by_id(cls, pk: int):
        """
        Delete stock data with given pk
        :param pk: StockData id
        :return: True if instance was deleted, else False
        """
        with pool_manager() as conn:
            query = f"DELETE FROM {cls._table} WHERE id = %(id)s "
            try:
                conn.cursor.execute(query, {'table': cls._table, 'id': pk})
                return True
            except(DataError, ProgrammingError):
                return False

    def to_dict(self):
        """
        Returns a dictionary with a stock data values.
        :return: Dictionary with instance data
        """
        return {'id': self.pk, "stock_id": self.stock_id, "price": self.price, "create_at": self.create_at}

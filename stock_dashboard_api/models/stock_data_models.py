from datetime import datetime
from psycopg2 import DataError, ProgrammingError

from stock_dashboard_api.utils.pool import pool_manager


class StockData:
    """
    Model used to create a StockData instance.
    """
    _table = "public.stocks_data"

    def __init__(self, stock_id: int, price: float, created_at: datetime, pk=None):
        """
        :param stock_id: Stock id
        :param price: StockData price
        :param created_at: StockData creation date, time
        :param pk: StockData id
        """
        self.pk = pk
        self.stock_id = stock_id
        self.price = price
        self.created_at = created_at

    @classmethod
    def create(cls, stock_id: int, price: float, created_at: datetime):
        """
        Create new stock data
        :param stock_id: Stock id
        :param price: StockData price
        :param created_at: StockData creation date, time
        :return: StockData instance
        """
        with pool_manager() as conn:
            query = f"""INSERT INTO {cls._table} (stock_id, price, created_at)
                        VALUES (%(stock_id)s, %(price)s, %(created_at)s)
                        RETURNING id, stock_id, price, created_at;"""
            try:
                conn.cursor.execute(query, {'stock_id': stock_id,
                                            'price': price,
                                            'created_at': created_at.strftime("%Y-%m-%d %H:%M:%S")})
                pk, stock_id, price, created_at = conn.cursor.fetchone()
                return StockData(pk=pk, stock_id=stock_id, price=price, created_at=created_at)
            except(DataError, ProgrammingError):
                return None

    def update(self, price=None, created_at=None):
        """
        Changes values of the stock data to the given.
        :param price: StockData price
        :param created_at: StockData creation date, time
        :return: updated StockData instance
        """
        data_to_update = []
        if price is not None:
            data_to_update.append("price = %(price)s")
        if created_at is not None:
            data_to_update.append("created_at = %(created_at)s")
            created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")
        query = f"""UPDATE {self._table} SET {', '.join(data_to_update)}
                    WHERE id = %(id)s 
                    RETURNING id, stock_id, price, created_at;"""
        with pool_manager() as conn:
            try:
                conn.cursor.execute(query, {'price': price,
                                            'created_at': created_at,
                                            'id': self.pk})
                contents = conn.cursor.fetchone()
                price = contents[2]
                created_at = contents[3]
                self.price = price
                self.created_at = created_at
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
                pk, stock_id, price, created_at = conn.cursor.fetchone()
                return StockData(pk=pk, stock_id=stock_id, price=price, created_at=created_at)
            except(DataError, ProgrammingError, TypeError):
                return None

    @classmethod
    def delete_by_id(cls, pk: int):
        """
        Delete stock data with given pk
        :param pk: StockData id
        :return: True if instance was deleted, else False
        """
        if not StockData.get_by_id(pk):
            return False
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
        """
        return {'id': self.pk, "stock_id": self.stock_id, "price": self.price, "created_at": self.created_at}

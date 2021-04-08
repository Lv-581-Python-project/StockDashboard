from stock_dashboard_api.utils.pool import pool_manager
from datetime import datetime
from psycopg2 import DataError, ProgrammingError


class StockData:
    _table = "public.stocks_data"

    def __init__(self, stock_id: int, price: float, create_at: datetime, pk=None):
        self.pk = pk
        self.stock_id = stock_id
        self.price = price
        self.create_at = create_at

    @classmethod
    def create(cls, stock_id: int, price: float, create_at: datetime):
        """
        Create new stock data
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
        """
        return {'id': self.pk, "stock_id": self.stock_id, "price": self.price, "create_at": self.create_at}
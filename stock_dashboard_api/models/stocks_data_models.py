from stock_dashboard_api.utils import pool as db


class StocksData:
    _table = "public.stocks_data"

    def __init__(self, stock_id, price, date_time, pk=None):
        self.pk = pk
        self.stock_id = stock_id
        self.price = price
        self.date_time = date_time

    @classmethod
    def create(cls, stock_id, price, date_time):
        with db.Connection() as conn:
            query = f"""INSERT INTO {cls._table} (stock_id, price, date_time)
                        VALUES (%(stock_id)s, %(price)s, %(date_time)s)
                        RETURNING id, stock_id, price, date_time;"""
            conn.cursor.execute(query, {'stock_id': stock_id, 'price': price, 'date_time': date_time})
            pk, stock_id, price, date_time = conn.cursor.fetchone()
            return StocksData(pk=pk, stock_id=stock_id, price=price, date_time=date_time)

    def update(self, price=None, date_time=None):
        query = f"UPDATE {self._table} SET "
        if price is not None:
            query += f"price = %(price)s"
            query += ", " if date_time is not None else " "
        if date_time is not None:
            query += f"date_time = %(date_time)s "
        query += f"WHERE id = %(pk)s RETURNING id, stock_id, price, date_time;"
        with db.Connection() as conn:
            conn.cursor.execute(query, {'price': price, 'date_time': date_time, "pk": self.pk})
            pk, stock_id, price, date_time = conn.cursor.fetchone()
            self.price = price
            self.date_time = date_time

    @classmethod
    def get_by_id(cls, pk):
        with db.Connection() as conn:
            query = f"SELECT id, stock_id, price, date_time FROM {cls._table} WHERE id = {pk};"
            conn.cursor.execute(query)
            pk, stock_id, price, date_time = conn.cursor.fetchone()
            return StocksData(pk=pk, stock_id=stock_id, price=price, date_time=date_time)

    @classmethod
    def delete_by_id(cls, pk):
        with db.Connection() as conn:
            query = f"DELETE FROM {cls._table} WHERE id = {pk};"
            conn.cursor.execute(query)

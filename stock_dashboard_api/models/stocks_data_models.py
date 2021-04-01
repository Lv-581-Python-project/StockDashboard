from stock_dashboard_api.utils import pool as db


class StocksData:
    _table = "public.stocks_data"

    def __init__(self, stock_id, price, create_at, pk=None):
        self.pk = pk
        self.stock_id = stock_id
        self.price = price
        self.create_at = create_at

    @classmethod
    def create(cls, stock_id, price, create_at):
        with db.Connection() as conn:
            query = f"""INSERT INTO {cls._table} (stock_id, price, create_at)
                        VALUES (%(stock_id)s, %(price)s, %(create_at)s)
                        RETURNING id, stock_id, price, create_at;"""
            conn.cursor.execute(query, {'stock_id': stock_id, 'price': price, 'create_at': create_at.strftime("%Y-%m-%d %H:%M:%S")})
            pk, stock_id, price, create_at = conn.cursor.fetchone()
            return StocksData(pk=pk, stock_id=stock_id, price=price, create_at=create_at)

    def update(self, price=None, create_at=None):
        query = f"UPDATE {self._table} SET "
        if price is not None:
            query += f"price = %(price)s"
            query += ", " if create_at is not None else " "
        if create_at is not None:
            query += f"create_at = %(create_at)s "
        query += f"WHERE id = %(pk)s RETURNING id, stock_id, price, create_at;"
        with db.Connection() as conn:
            conn.cursor.execute(query, {'price': price, 'create_at': create_at.strftime("%Y-%m-%d %H:%M:%S"), "pk": self.pk})
            pk, stock_id, price, create_at = conn.cursor.fetchone()
            self.price = price
            self.create_at = create_at

    @classmethod
    def get_by_id(cls, pk):
        with db.Connection() as conn:
            query = f"SELECT id, stock_id, price, create_at FROM {cls._table} WHERE id = {pk};"
            conn.cursor.execute(query)
            pk, stock_id, price, create_at = conn.cursor.fetchone()
            return StocksData(pk=pk, stock_id=stock_id, price=price, create_at=create_at)

    @classmethod
    def delete_by_id(cls, pk):
        with db.Connection() as conn:
            query = f"DELETE FROM {cls._table} WHERE id = {pk};"
            conn.cursor.execute(query)

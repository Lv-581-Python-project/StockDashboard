from stock_dashboard_api.utils.pool import pool_manager


class StockData:
    _table = "public.stocks_data"

    def __init__(self, stock_id, price, create_at, pk=None):
        self.pk = pk
        self.stock_id = stock_id
        self.price = price
        self.create_at = create_at

    @classmethod
    def create(cls, stock_id, price, create_at):
        with pool_manager() as conn:
            query = f"""INSERT INTO {cls._table} (stock_id, price, create_at)
                        VALUES (%(stock_id)s, %(price)s, %(create_at)s)
                        RETURNING id, stock_id, price, create_at;"""
            conn.cursor.execute(query, {'stock_id': stock_id,
                                        'price': price,
                                        'create_at': create_at.strftime("%Y-%m-%d %H:%M:%S")})
            pk, stock_id, price, create_at = conn.cursor.fetchone()
            return StockData(pk=pk, stock_id=stock_id, price=price, create_at=create_at)

    def update(self, price=None, create_at=None):
        list_with_variable = []
        if price is not None:
            list_with_variable.append("price = %(price)s")
        if create_at is not None:
            list_with_variable.append("create_at = %(create_at)s")
        query = f"""UPDATE {self._table} SET {', '.join(list_with_variable)}
                    WHERE id = %(id)s 
                    RETURNING id, stock_id, price, create_at;"""
        with pool_manager() as conn:
            conn.cursor.execute(query, {'price': price,
                                        'create_at': create_at.strftime("%Y-%m-%d %H:%M:%S"),
                                        'id': self.pk})
            pk, stock_id, price, create_at = conn.cursor.fetchone()
            self.price = price
            self.create_at = create_at

    @classmethod
    def get_by_id(cls, pk):
        with pool_manager() as conn:
            query = f"SELECT id, stock_id, price, create_at FROM {cls._table} WHERE id = %(id)s"
            conn.cursor.execute(query, {'id': pk})
            pk, stock_id, price, create_at = conn.cursor.fetchone()
            return StockData(pk=pk, stock_id=stock_id, price=price, create_at=create_at)

    @classmethod
    def delete_by_id(cls, pk):
        with pool_manager() as conn:
            query = f"DELETE FROM {cls._table} WHERE id = %(id)s "
            conn.cursor.execute(query, {'table': cls._table, 'id': pk})

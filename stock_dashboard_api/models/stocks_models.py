from stock_dashboard_api.utils.pool import pool_manager


class Stocks:
    _table = 'public.stocks'

    def __init__(self, name, company_name, pk=None):
        self.pk = pk
        self.name = name
        self.company_name = company_name

    @classmethod
    def create(cls, name, company_name):
        with pool_manager() as conn:
            query = f"""INSERT INTO {cls._table} (name, company_name)
                        VALUES (%(name)s, %(company_name)s)
                        RETURNING id, name, company_name;"""
            conn.cursor.execute(query, {'name': name, 'company_name': company_name})
            pk, name, company_name = conn.cursor.fetchone()
            return Stocks(pk=pk, name=name, company_name=company_name)

    def update(self, name=None, company_name=None):
        list_with_variable = []
        if name is not None:
            list_with_variable.append("name = %(name)s")
        if company_name is not None:
            list_with_variable.append("company_name = %(company_name)s")
        query = f"""UPDATE {self._table} SET {', '.join(list_with_variable)}
                WHERE id = %(pk)s RETURNING id, name, company_name; """
        with pool_manager() as conn:
            conn.cursor.execute(
                query,
                {'name': name, 'company_name': company_name, 'pk': self.pk})
            pk, name, company_name = conn.cursor.fetchone()
            self.name = name
            self.company_name = company_name

    @classmethod
    def delete_by_id(cls, pk):
        with pool_manager() as conn:
            query = f"DELETE FROM {cls._table} WHERE id = %(id)s;"
            conn.cursor.execute(query, {'id': pk})

    @classmethod
    def get_by_id(cls, pk):
        with pool_manager() as conn:
            query = f"SELECT id, name, company_name FROM {cls._table} WHERE id = %(id)s "
            conn.cursor.execute(query, {'id': pk})
            pk, name, company_name = conn.cursor.fetchone()
            return Stocks(pk=pk, name=name, company_name=company_name)

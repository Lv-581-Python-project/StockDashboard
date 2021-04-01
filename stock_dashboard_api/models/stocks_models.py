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
        query = [f"UPDATE {self._table} SET ", ]
        query_list = ["name = %(name)s", ", ", " ", "company_name = %(company_name)s ",
                      "WHERE id = %(pk)s RETURNING id, name, company_name; "]
        if name is not None:
            query.append(query_list[0])
            if company_name is not None:
                query.append(query_list[1])
            else:
                query.append(query_list[2])
        if company_name is not None:
            query.append(query_list[3])
        query.append(query_list[4])
        with pool_manager() as conn:
            conn.cursor.execute(
                ''.join(query),
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

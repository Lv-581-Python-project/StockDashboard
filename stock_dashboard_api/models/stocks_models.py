from stock_dashboard_api.utils import pool as db


class Stocks:

    def __init__(self, name, company_name, pk=None):
        self.pk = pk
        self.name = name
        self.company_name = company_name

    @classmethod
    def create(cls, name, company_name):
        with db.Connection() as conn:
            query = """INSERT INTO public.stocks (name, company_name)
                        VALUES (%(name)s, %(company_name)s)
                        RETURNING id, name, company_name;"""
            conn.cursor.execute(query, {'name': name, 'company_name': company_name})
            pk, name, company_name = conn.cursor.fetchone()
            return Stocks(pk=pk, name=name, company_name=company_name)

    def update(self, name=None, company_name=None):
        query = "UPDATE public.stocks SET "
        if name is not None:
            query += "name = %(name)s"
            query += ", " if company_name is not None else " "
        if company_name is not None:
            query += "company_name = %(company_name)s "
        query += "WHERE id = %(pk)s RETURNING id, name, company_name; "
        with db.Connection() as conn:
            conn.cursor.execute(query, {'name': name, 'company_name': company_name, 'pk': self.pk})
            pk, name, company_name = conn.cursor.fetchone()
            self.name = name
            self.company_name = company_name

    @classmethod
    def delete_by_id(cls, pk):
        with db.Connection() as conn:
            query = f"DELETE FROM public.stocks WHERE id = %(id)s;"
            conn.cursor.execute(query, {'id': pk})

    @classmethod
    def get_by_id(cls, pk):
        with db.Connection() as conn:
            query = f"SELECT id, name, company_name FROM public.stocks WHERE id = %(id)s "
            conn.cursor.execute(query, {'id': pk})
            pk, name, company_name = conn.cursor.fetchone()
            return Stocks(pk=pk, name=name, company_name=company_name)

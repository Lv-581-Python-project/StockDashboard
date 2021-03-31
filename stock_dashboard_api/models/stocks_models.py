from StockDashboardAPI.utils import pool as db


class Stocks:
    __table = 'public.stocks'

    def __init__(self, name, company_name, pk=None):
        self.pk = pk
        self.name = name
        self.company_name = company_name

    @classmethod
    def create(cls, name, company_name):
        with db.Connection() as conn:
            query = f"""INSERT INTO {cls.__table} (name, company_name)
                        VALUES ('{name}', '{company_name}')
                        RETURNING id, name, company_name;"""
            conn.cursor.execute(query)
            pk, name, company_name = conn.cursor.fetchone()
            return Stocks(pk=pk, name=name, company_name=company_name)

    def update(self, name=None, company_name=None):
        query = f"UPDATE {self.__table} SET "
        if name is not None:
            query += f"name = {name}"
            query += ", " if company_name is not None else " "
        if company_name is not None:
            query += f"company_name = {company_name} "
        query += f"WHERE id = {self.pk} RETURNING id, name, company_name; "
        with db.Connection() as conn:
            conn.cursor.execute(query)
            pk, name, company_name = conn.cursor.fetchone()
            self.name = name
            self.company_name = company_name

    @classmethod
    def delete_by_id(cls, pk):
        with db.Connection() as conn:
            conn.query = f"DELETE FROM {cls.__table} WHERE id = {pk};"
            conn.cursor.execute(query)

    @classmethod
    def get_by_id(cls, pk):
        with db.Connection() as conn:
            query = f"SELECT id, name, company_name FROM {cls.__table} WHERE id = {pk} "
            conn.cursor.execute(query)
            pk, name, company_name = conn.cursor.fetchone()
            return Stocks(pk=pk, name=name, company_name=company_name)

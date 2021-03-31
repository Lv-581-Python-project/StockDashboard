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
            cursor = conn.cursor()
            query = f"""INSERT INTO {cls.__table} (name, company_name)
                        VALUES ('{name}', '{company_name}')
                        RETURNING id, name, company_name;"""
            cursor.execute(query)
            pk, name, company_name = cursor.fetchone()
            conn.commit()
            cursor.close()
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
            cursor = conn.cursor()
            cursor.execute(query)
            _pk, _name, _company_name = cursor.fetchone()
            self.name = _name
            self.company_name = _company_name
            conn.commit()
            cursor.close()

    @classmethod
    def delete_by_id(cls, pk):
        with db.Connection() as conn:
            cursor = conn.cursor()
            query = f"DELETE FROM {cls.__table} WHERE id = {pk};"
            cursor.execute(query)
            conn.commit()
            cursor.close()

    @classmethod
    def get_by_id(cls, pk):
        with db.Connection() as conn:
            cursor = conn.cursor()
            query = f"SELECT id, name, company_name FROM {cls.__table} WHERE id = {pk} "
            cursor.execute(query)
            _pk, _name, _company_name = cursor.fetchone()
            cursor.close()
            return Stocks(pk=_pk, name=_name, company_name=_company_name)

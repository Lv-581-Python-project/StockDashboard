from StockDashboardAPI.utils import pool as db

class Stocks:
    def __init__(self):
        self.name = str()
        self.company_name = str()

    def create(self, name,company_name):
        with db.Connection() as conn:
            cursor = conn.cursor()
            query = f"INSERT INTO public.stocks (name, company_name) VALUES ('%s', '%s');"%(name, company_name)
            cursor.execute(query)
            conn.commit()
            cursor.close()

    def update(self,id,name=None,company_name=None):
        if not name:
            with db.Connection() as conn:
                cursor = conn.cursor()
                query = f"UPDATE public.stocks SET company_name = '%s' WHERE id = %s;"%(company_name, id)
                cursor.execute(query)
                conn.commit()
                cursor.close()
        if not company_name:
            with db.Connection() as conn:
                cursor = conn.cursor()
                query = f"UPDATE public.stocks SET name = '%s' WHERE id = %s;"%(name, id)
                cursor.execute(query)
                conn.commit()
                cursor.close()

    def remove(self, id):
        with db.Connection() as conn:
            cursor = conn.cursor()
            query = f"DELETE FROM public.stocks WHERE id = %s;" % (id)
            cursor.execute(query)
            conn.commit()
            cursor.close()

    def get_by_id(self, id):
        with db.Connection() as conn:
            cursor = conn.cursor()
            query = f"SELECT name, company_name FROM public.stocks WHERE id = %s;" % (id)
            cursor.execute(query)
            record = cursor.fetchall()
            print(record)
            cursor.close()

import pool as db

def create(name,company_name):
    with db.pool_manager() as conn:
        cursor = conn.cursor()
        query = f"INSERT INTO public.stocks (name, company_name) VALUES ('%s', '%s');"%(name, company_name)
        cursor.execute(query)
        conn.commit()
        cursor.close()

def update(id,name=None,company_name=None):
    if not name:
        with db.pool_manager() as conn:
            cursor = conn.cursor()
            query = f"UPDATE public.stocks SET company_name = '%s' WHERE id = %s;"%(company_name, id)
            cursor.execute(query)
            conn.commit()
            cursor.close()
    if not company_name:
        with db.pool_manager() as conn:
            cursor = conn.cursor()
            query = f"UPDATE public.stocks SET name = '%s' WHERE id = %s;"%(name, id)
            cursor.execute(query)
            conn.commit()
            cursor.close()

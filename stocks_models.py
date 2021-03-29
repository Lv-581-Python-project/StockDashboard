import pool as db

def create(name,company_name):
    with db.pool_manager() as conn:
        cursor = conn.cursor()
        query = f"INSERT INTO public.stocks (name, company_name) VALUES ('%s', '%s');"%(name, company_name)
        cursor.execute(query)
        conn.commit()
        cursor.close()
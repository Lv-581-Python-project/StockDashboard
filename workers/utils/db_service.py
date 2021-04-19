from pool import pool_manager
from psycopg2 import DataError, ProgrammingError


def in_use_check(stocks_name):
    """
    Function to look at in_use flag
    :param stocks_name: name of company
    :return: in_use
    """
    with pool_manager() as conn:
        query = f"""SELECT in_use
                    FROM stocks
                    WHERE name = %(stocks_name)s"""
        try:
            conn.cursor.execute(query, {"stocks_name": stocks_name})
            in_use = conn.cursor.fetchone()
            return in_use[0]
        except (DataError, ProgrammingError, TypeError):
            return None


def get_id(stocks_name):
    """
    Function to get id of stock
    :param stocks_name: name of company
    :return: id
    """
    with pool_manager() as conn:
        query = f"""SELECT id
                    FROM stocks
                    WHERE name = %(stocks_name)s"""
        try:
            conn.cursor.execute(query, {"stocks_name": stocks_name})
            pk = conn.cursor.fetchone()
            return pk[0]
        except (DataError, ProgrammingError, TypeError):
            return None


def in_use_change(pk):
    """
    Function to change in_use flag
    :param pk: id of stock
    :return: True if success and None if not
    """
    with pool_manager() as conn:
        query = f"""UPDATE stocks
                    SET in_use = true 
                    WHERE id = %(id)s
                    RETURNING id, in_use"""
        try:
            conn.cursor.execute(query, {"id": pk})
            conn.cursor.fetchone()
            return True
        except (DataError, ProgrammingError, TypeError):
            return None


def insert_new_stock(name, company_name):
    """
    Function to insert data about new stock
    :param name: name of company on the stock
    :param company_name: company name
    :return: True if success and None if not
    """
    with pool_manager() as conn:
        query = f"""INSERT INTO stocks(name, company_name)
                    VALUES 
                    (%(name)s, %(company_name)s)
                    RETURNING id, in_use"""
        try:
            conn.cursor.execute(query, {"name": name, "company_name": company_name})
            conn.cursor.fetchone()
            return True
        except (DataError, ProgrammingError, TypeError):
            return None


def insert_stock_data(stock_id, price, created_at):
    with pool_manager() as conn:
        query = f"""INSERT INTO stocks_data(stock_id, price, created_at)
                    VALUES 
                    (%(stock_id)s, %(price)s, %(created_at)s)
                    RETURNING id"""
        try:
            conn.cursor.execute(query, {"stock_id": stock_id, "price": price, "created_at" : created_at})
            conn.cursor.fetchone()
            return True
        except (DataError, ProgrammingError, TypeError):
            return None
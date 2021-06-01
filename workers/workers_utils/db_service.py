from psycopg2 import DataError, ProgrammingError

from workers.workers_utils.logger import pool_logger as logger
from workers.workers_utils.pool import pool_manager


def stock_in_use_check(stocks_name):
    """
    Function to look at in_use flag
    :param stocks_name: name of company
    :return: in_use
    """
    with pool_manager() as conn:
        query = """SELECT in_use
                    FROM stocks
                    WHERE name = %(stocks_name)s"""
        try:
            conn.cursor.execute(query, {"stocks_name": stocks_name})
            in_use = conn.cursor.fetchone()
            return in_use[0]
        except (DataError, ProgrammingError, TypeError):
            logger.info("stock_in_use_check: maybe wrong stock_name")


def stock_get_id(stocks_name):
    """
    Function to get id of stock
    :param stocks_name: name of company
    :return: id
    """
    with pool_manager() as conn:
        query = """SELECT id
                    FROM stocks
                    WHERE name = %(stocks_name)s"""
        try:
            conn.cursor.execute(query, {"stocks_name": stocks_name})
            pk = conn.cursor.fetchone()
            return pk[0]
        except (DataError, ProgrammingError, TypeError):
            logger.info("stock_get_id: maybe wrong id")


def stock_in_use_change(pk):
    """
    Function to change in_use flag
    :param pk: id of stock
    :return: True if success and None if not
    """
    with pool_manager() as conn:
        query = """UPDATE stocks
                    SET in_use = true 
                    WHERE id = %(id)s
                    RETURNING id, in_use"""
        try:
            conn.cursor.execute(query, {"id": pk})
            conn.cursor.fetchone()
            return True
        except (DataError, ProgrammingError, TypeError):
            logger.info("stock_in_use_change: maybe wrong id")


def insert_new_stock(name, company_name, country, industry, sector):
    """
    Function to insert data about new stock
    :param name: name of company on the stock
    :param company_name: company name
    :param country: country of company
    :param industry: industry
    :param sector: sector
    :return: True if success and None if not
    """
    with pool_manager() as conn:
        query = """INSERT INTO stocks(name, company_name, country, industry, sector)
                    VALUES 
                    (%(name)s, %(company_name)s, %(country)s, %(industry)s, %(sector)s )
                    RETURNING id, in_use"""
        try:
            conn.cursor.execute(query, {"name": name,
                                        "company_name": company_name,
                                        "country": country,
                                        "industry": industry,
                                        "sector": sector})
            conn.cursor.fetchone()
            return True
        except (DataError, ProgrammingError, TypeError):
            logger.info("insert_new_stock: maybe wrong name or company name")


def insert_stock_data(stock_id, price, created_at):
    """
    Function to insert data about stock
    :param stock_id: id of stock
    :param price: price of a stock
    :param created_at: time to creation
    :return: True if success and None if not
    """
    with pool_manager() as conn:
        query = """INSERT INTO stocks_data(stock_id, price, created_at)
                    VALUES 
                    (%(stock_id)s, %(price)s, %(created_at)s)
                    RETURNING id"""
        try:
            conn.cursor.execute(query, {"stock_id": stock_id, "price": price, "created_at": created_at})
            conn.cursor.fetchone()
            return True
        except (DataError, ProgrammingError, TypeError):
            logger.info("insert_stock_data: maybe wrong parameters")


def get_all_stocks_name():
    """
    Function to return set of all stocks names
    :return: set of all stocks names
    """
    with pool_manager() as conn:
        query = """SELECT name
                     FROM stocks"""
        try:
            conn.cursor.execute(query)
            stock_names = conn.cursor.fetchall()
            stock_names = set(map(lambda x: x[0], stock_names))
            return stock_names
        except (DataError, ProgrammingError, TypeError):
            logger.info("get_all_stocks_name: fail to get data")


def get_all_stocks_in_use():
    """
    Function to find all stocks in use
    :return: List of dicts with ids and names
    """
    with pool_manager() as conn:
        query = """SELECT id, name
                     FROM stocks
                     WHERE in_use = true"""
        try:
            conn.cursor.execute(query)
            data = conn.cursor.fetchall()
            stocks_in_use = list()
            list(map(lambda x: stocks_in_use.append({"id": x[0], "name": x[1]}), data))
            return stocks_in_use
        except (DataError, ProgrammingError, TypeError):
            logger.info("get_all_stocks_in_use: fail to get data")


def get_stocks_data_last_record(stock_id):
    """
    Get the date of the latest update by stock_id
    :param stock_id: id of stock
    :return: the latest update
    """
    with pool_manager() as conn:
        query = """SELECT created_at
                     FROM stocks_data
                     WHERE stock_id = (%(stock_id)s)"""
        try:
            conn.cursor.execute(query, {"stock_id": stock_id})
            data = conn.cursor.fetchall()
            latest_update = max(list(map(lambda x: x[0], data)))
            return latest_update
        except (DataError, ProgrammingError, TypeError):
            logger.info("get_stocks_data_last_record: fail to get data")

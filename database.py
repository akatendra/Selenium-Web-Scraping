import contextlib
import sqlite3
import logging.config

# Set up logging
logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def execute_sql_query(sql, data=None):
    with contextlib.closing(sqlite3.connect('avito_database.sqlite',
                                            detect_types=sqlite3.PARSE_DECLTYPES |
                                                         sqlite3.PARSE_COLNAMES
                                            )
                            ) as connection, connection, contextlib.closing(
        connection.cursor()) as cursor:
        if data is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, data)
        return cursor.fetchall()


def create_main_table():
    sql_create_main_table = '''
                            CREATE TABLE IF NOT EXISTS items (
                            id INTEGER PRIMARY KEY, 
                            data_item_id INTEGER,
                            item_id TEXT,
                            item_url TEXT,
                            item_title TEXT,
                            item_type TEXT,
                            item_number_of_rooms INTEGER,
                            item_area REAL,
                            item_floor_house TEXT,
                            item_floor INTEGER,
                            item_floors_in_house INTEGER,
                            item_price INTEGER,
                            item_currency TEXT,
                            item_address TEXT,
                            item_city TEXT,
                            property_type TEXT,
                            item_date TIMESTAMP,
                            item_add_date TIMESTAMP
                            );'''
    execute_sql_query(sql_create_main_table)
    logger.info('Main table created!')


def get_item_ids():
    sql_get_item_ids = 'SELECT item_id FROM items;'
    item_ids = execute_sql_query(sql_get_item_ids)
    item_ids_tuple = set((item[0] for item in item_ids))
    logger.debug(f'Items_ids tuple received: {len(item_ids_tuple)}')
    return item_ids_tuple


def get_item_ids_list():
    sql_get_item_ids = 'SELECT item_id FROM items;'
    item_ids = execute_sql_query(sql_get_item_ids)
    item_ids = list((item[0] for item in item_ids))
    logger.debug(f'Items_ids list received: {len(item_ids)}')
    return item_ids


def write_to_database(data):
    sql_put_data = '''
                   INSERT INTO items
                   ('data_item_id', 
                    'item_id', 
                    'item_url', 
                    'item_title',
                    'item_type', 
                    'item_number_of_rooms', 
                    'item_area', 
                    'item_floor_house', 
                    'item_floor', 
                    'item_floors_in_house', 
                    'item_price', 
                    'item_currency', 
                    'item_address', 
                    'item_city',
                    'property_type',
                    'item_date', 
                    'item_add_date') 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                   '''
    item_ids = set(data.keys())
    # logger.debug(f'{type(item_ids)}, {len(item_ids)}, {item_ids}')
    item_ids_database = get_item_ids()
    item_ids_to_write = item_ids.difference(item_ids_database)
    for item_id in item_ids_to_write:
        # logger.debug(f'item_id: {item_id}')
        data_tuple = tuple((item_data for item_data in data[item_id].values()))
        # logger.debug(f'{type(data_tuple)}, {data_tuple}')
        execute_sql_query(sql_put_data, data_tuple)
    logger.info('Data saved into database!')


def duplicates_check():
    item_ids = get_item_ids()
    logger.debug(f'{type(item_ids)}, {len(item_ids)}, {item_ids}')
    item_ids_list = get_item_ids_list()
    logger.debug(
        f'{type(item_ids_list)}, {len(item_ids_list)}, {item_ids_list}')


if __name__ == '__main__':
    # create_main_table()
    duplicates_check()

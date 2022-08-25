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


def create_table_kvartiry_vtorichka():
    sql_create_table_kvartiry_vtorichka = '''
                            CREATE TABLE IF NOT EXISTS kvartiry_vtorichka (
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
    execute_sql_query(sql_create_table_kvartiry_vtorichka)
    logger.info('Table kvartiry_vtorichka created!')


def create_table_kvartiry_novostroyka():
    sql_create_table_kvartiry_novostroyka = '''
                            CREATE TABLE IF NOT EXISTS kvartiry_novostroyka (
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
                            item_development_name TEXT,
                            item_address TEXT,
                            item_city TEXT,
                            property_type TEXT,
                            item_date TIMESTAMP,
                            item_add_date TIMESTAMP
                            );'''
    execute_sql_query(sql_create_table_kvartiry_novostroyka)
    logger.info('Table kvartiry_novostroyka created!')


def get_item_ids(table):
    sql_get_item_ids = f'SELECT item_id FROM {table};'
    item_ids = execute_sql_query(sql_get_item_ids)
    item_ids_tuple = set((item[0] for item in item_ids))
    logger.debug(f'Items_ids tuple received: {len(item_ids_tuple)}')
    return item_ids_tuple


def get_item_ids_list(table):
    sql_get_item_ids = f'SELECT item_id FROM {table};'
    item_ids = execute_sql_query(sql_get_item_ids)
    item_ids = list((item[0] for item in item_ids))
    logger.debug(f'Items_ids list received: {len(item_ids)}')
    return item_ids


def write_to_db_kvartiry_vtorichka(data):
    table = 'kvartiry_vtorichka'
    sql_put_data = f'''
                   INSERT INTO {table}
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
    item_ids_database = get_item_ids(table)
    # item_ids_to_write = item_ids.difference(item_ids_database)
    # for item_id in item_ids_to_write:
    for item_id in item_ids:
        # logger.debug(f'item_id: {item_id}')
        # Check if item_id is already exist in database
        if item_id not in item_ids_database:
            data_tuple = tuple(
                (item_data for item_data in data[item_id].values()))
            # logger.debug(f'{type(data_tuple)}, {data_tuple}')
            execute_sql_query(sql_put_data, data_tuple)
    logger.info('Data saved into table kvartiry_vtorichka!')


def write_to_db_kvartiry_novostroyka(data):
    table = 'kvartiry_novostroyka'
    sql_put_data = f'''
                   INSERT INTO {table}
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
                    'item_development_name',
                    'item_address', 
                    'item_city',
                    'property_type',
                    'item_date', 
                    'item_add_date') 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                   '''
    item_ids = set(data.keys())
    # logger.debug(f'{type(item_ids)}, {len(item_ids)}, {item_ids}')
    item_ids_database = get_item_ids(table)
    item_ids_to_write = item_ids.difference(item_ids_database)
    for item_id in item_ids_to_write:
        # logger.debug(f'item_id: {item_id}')
        data_tuple = tuple((item_data for item_data in data[item_id].values()))
        # logger.debug(f'{type(data_tuple)}, {data_tuple}')
        execute_sql_query(sql_put_data, data_tuple)
    logger.info('Data saved into table kvartiry_novostroyka!')


def duplicates_check(table):
    item_ids = get_item_ids(table)
    logger.debug(f'{type(item_ids)}, {len(item_ids)}, {item_ids}')
    item_ids_list = get_item_ids_list(table)
    logger.debug(
        f'{type(item_ids_list)}, {len(item_ids_list)}, {item_ids_list}')


def get_item_count_per_day(table):
    sql_get_item_count_per_day = f'''
                                 SELECT 
                                     STRFTIME('%Y-%m-%d', item_date), 
                                     COUNT(*) 
                                 FROM 
                                    {table} 
                                 GROUP BY 
                                    STRFTIME('%Y-%m-%d', item_date);
                                 '''
    item_count_per_day = execute_sql_query(sql_get_item_count_per_day)
    logger.debug(
        f'item_count_per_day received: {len(item_count_per_day)} | {item_count_per_day}')
    return item_count_per_day


def get_item_count_per_day2(table):
    sql_get_item_count_per_day = f'''
                                 SELECT 
                                     STRFTIME('%Y-%m-%d', item_date) 
                                 FROM 
                                    {table};
                                 '''
    item_count_per_day = execute_sql_query(sql_get_item_count_per_day)
    # logger.debug(
    #     f'item_count_per_day received: {len(item_count_per_day)} | {item_count_per_day}')
    return item_count_per_day

def get_item_date_price_area(table):
    sql_get_item_date_price_area = f'''
                                 SELECT
                                     STRFTIME('%Y-%m-%d', item_date),
                                     item_price,
                                     item_area
                                 FROM 
                                    {table};
                                 '''
    item_date_price_area = execute_sql_query(sql_get_item_date_price_area)
    # logger.debug(
    #     f'item_date_price_area received: {len(item_date_price_area)} | {item_date_price_area}')
    return item_date_price_area

def get_item_date_price_area_average(table):
    sql_get_item_date_price_area_av = f'''
                                 SELECT
                                     STRFTIME('%Y-%m-%d', item_date),
                                     round(AVG(item_price / item_area), 0) AS av_price_per_sq_m
                                 FROM 
                                    {table}
                                 GROUP BY 
                                    STRFTIME('%Y-%m-%d', item_date);
                                 '''
    item_date_price_area_av = execute_sql_query(sql_get_item_date_price_area_av)
    # logger.debug(
    #     f'item_date_price_area_av received: {len(item_date_price_area_av)} | {item_date_price_area_av}')
    return item_date_price_area_av


# def rename_table_items():
#     sql_rename_table_items = '''
#                            ALTER TABLE items
#                            RENAME TO kvartiry_vtorichka;
#                            '''
#     execute_sql_query(sql_rename_table_items)


if __name__ == '__main__':
    # create_main_table()
    # duplicates_check('kvartiry_vtorichka')
    # duplicates_check('kvartiry_novostroyka')
    # rename_table_items()
    # create_table_kvartiry_novostroyka()
    # get_item_ids('kvartiry_vtorichka')
    # get_item_ids_list('kvartiry_vtorichka')
    print(get_item_count_per_day('kvartiry_vtorichka'))

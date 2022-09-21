import contextlib
import sqlite3
import logging.config

# Set up logging
logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def execute_sql_query(sql, data=None):
    with contextlib.closing(sqlite3.connect('avito_database.sqlite3',
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


def create_table_doma_dachi_kottedzhi():
    sql_create_table_doma_dachi_kottedzhi = '''
                            CREATE TABLE IF NOT EXISTS doma_dachi_kottedzhi (
                            id INTEGER PRIMARY KEY, 
                            data_item_id INTEGER,
                            item_id TEXT,
                            item_url TEXT,
                            item_title TEXT,
                            item_type TEXT,
                            item_area REAL,
                            item_land_area TEXT,
                            item_price INTEGER,
                            item_currency TEXT,
                            item_address TEXT,
                            item_city TEXT,
                            property_type TEXT,
                            item_date TIMESTAMP,
                            item_add_date TIMESTAMP
                            );'''
    execute_sql_query(sql_create_table_doma_dachi_kottedzhi)
    logger.info('Table doma_dachi_kottedzhi created!')


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


def write_to_db_doma_dachi_kottedzhi(data):
    table = 'doma_dachi_kottedzhi'
    sql_put_data = f'''
                   INSERT INTO {table}
                   ('data_item_id', 
                    'item_id', 
                    'item_url', 
                    'item_title',
                    'item_type', 
                    'item_area',
                    'item_land_area', 
                    'item_price', 
                    'item_currency',
                    'item_address', 
                    'item_city',
                    'property_type',
                    'item_date', 
                    'item_add_date') 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
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
    logger.info('Data saved into table doma_dachi_kottedzhi!')


def duplicates_check(table):
    item_ids = get_item_ids(table)
    logger.debug(f'{type(item_ids)}, {len(item_ids)}, {item_ids}')
    item_ids_list = get_item_ids_list(table)
    logger.debug(
        f'{type(item_ids_list)}, {len(item_ids_list)}, {item_ids_list}')


###############################################################################
######################## VISUALISATION QUERIES ################################
###############################################################################
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
    # logger.debug(
    #     f'item_count_per_day received: {len(item_count_per_day)} | {item_count_per_day}')
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


def get_item_count_per_day3():
    sql_get_item_count_per_day = f'''
                                    SELECT STRFTIME('%Y-%m-%d', item_date),
                                    property_type
                                    FROM 'kvartiry_vtorichka'
                                    UNION ALL
                                    SELECT STRFTIME('%Y-%m-%d', item_date),
                                    property_type
                                    FROM 'kvartiry_novostroyka'
                                    UNION ALL
                                    SELECT STRFTIME('%Y-%m-%d', item_date),
                                    property_type
                                    FROM 'doma_dachi_kottedzhi'
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
    item_date_price_area_av = execute_sql_query(
        sql_get_item_date_price_area_av)
    # logger.debug(
    #     f'item_date_price_area_av received: {len(item_date_price_area_av)} | {item_date_price_area_av}')
    return item_date_price_area_av


def get_item_date_price_area_average_union():
    sql_get_item_date_price_area_av_union = f'''
                                            SELECT STRFTIME('%Y-%m-%d', item_date),
                                                   round(AVG(item_price / item_area), 0) AS av_price_per_sq_m,
                                                   property_type
                                            FROM 'kvartiry_vtorichka'
                                            GROUP BY STRFTIME('%Y-%m-%d', item_date)
                                            UNION
                                            SELECT STRFTIME('%Y-%m-%d', item_date),
                                                   round(AVG(item_price / item_area), 0) AS av_price_per_sq_m,
                                                   property_type
                                            FROM 'kvartiry_novostroyka'
                                            GROUP BY STRFTIME('%Y-%m-%d', item_date)
                                            UNION
                                            SELECT STRFTIME('%Y-%m-%d', item_date),
                                                   round(AVG(item_price / item_area), 0) AS av_price_per_sq_m,
                                                   property_type
                                            FROM 'doma_dachi_kottedzhi'
                                            GROUP BY STRFTIME('%Y-%m-%d', item_date);
                                            '''
    item_date_price_area_av_union = execute_sql_query(
        sql_get_item_date_price_area_av_union)
    # logger.debug(
    #     f'item_date_price_area_av received: {len(item_date_price_area_av_union)} | {item_date_price_area_av_union}')
    return item_date_price_area_av_union


def get_item_count_by_cities(table):
    sql_get_item_count_by_cities = f'''
                                 SELECT
                                     item_city
                                 FROM 
                                    {table};
                                 '''
    item_count_by_cities = execute_sql_query(sql_get_item_count_by_cities)
    # logger.debug(
    #     f'item_date_price_area_av received: {len(item_count_by_cities)} | {item_count_by_cities}')
    return item_count_by_cities


def get_top10_cities(table):
    sql_get_order_vector = f'''
                            SELECT item_city
                            FROM
                              (SELECT item_city,
                                      COUNT(*) AS item_count
                               FROM {table}
                               GROUP BY item_city
                               ORDER BY item_count DESC
                               LIMIT 10)
                            '''
    order_vector = execute_sql_query(sql_get_order_vector)
    order_vector = list((item[0] for item in order_vector))
    # logger.debug(
    #     f'item_date_price_area_av received: {len(order_vector)} | {order_vector}')
    sql_get_top10_cities = f'''
                            SELECT item_city
                            FROM {table}
                            WHERE item_city IN
                                (SELECT item_city
                                 FROM
                                   (SELECT item_city,
                                           COUNT(*)
                                    FROM {table}
                                    GROUP BY item_city
                                    ORDER BY COUNT(*) DESC
                                    LIMIT 10))
                                    ;
                                 '''
    top10_cities = execute_sql_query(sql_get_top10_cities)
    # logger.debug(
    #     f'item_date_price_area_av received: {len(top10_cities)} | {top10_cities}')
    return order_vector, top10_cities


def get_item_count_sevastopol(table):
    sql_get_item_count_sevastopol = f'''
                                 SELECT
                                     STRFTIME('%Y-%m-%d', item_date),
                                     COUNT(*)
                                 FROM 
                                    {table}
                                 WHERE
                                     item_city = 'Севастополь'
                                 GROUP BY 
                                    STRFTIME('%Y-%m-%d', item_date)
                                 ORDER BY
                                     STRFTIME('%Y-%m-%d', item_date)
                                 '''
    item_count_sevastopol = execute_sql_query(sql_get_item_count_sevastopol)
    # logger.debug(
    #     f'item_date_price_area_av received: {len(item_count_sevastopol)} | {item_count_sevastopol}')
    return item_count_sevastopol


def get_item_count_sevastopol_simple(table):
    sql_get_item_count_sevastopol = f'''
                                 SELECT
                                     STRFTIME('%Y-%m-%d', item_date)
                                 FROM 
                                    {table}
                                 WHERE
                                     item_city LIKE '%Севастополь%'
                                 ORDER BY
                                     STRFTIME('%Y-%m-%d', item_date)
                                 '''
    item_count_sevastopol = execute_sql_query(sql_get_item_count_sevastopol)
    # logger.debug(
    #     f'item_date_price_area_av received: {len(item_count_sevastopol)} | {item_count_sevastopol}')
    return item_count_sevastopol


def get_item_cities():
    sql_get_item_cities = f'''
                            SELECT
                                item_city
                            FROM
                                'kvartiry_vtorichka'
                            GROUP BY
                                item_city
                            UNION
                            SELECT
                                item_city
                            FROM
                                'kvartiry_novostroyka'
                            GROUP BY 
                                item_city                                     
                                     '''
    item_cities = execute_sql_query(sql_get_item_cities)
    # logger.debug(
    #     f'item_date_price_area_av received: {len(item_cities)} | {item_cities}')
    return item_cities


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
    # print(get_item_count_per_day('kvartiry_vtorichka'))
    # get_item_count_by_cities('kvartiry_vtorichka')
    # get_top10_cities('kvartiry_vtorichka')
    # get_item_count_sevastopol('kvartiry_vtorichka')
    # get_item_date_price_area_average('kvartiry_vtorichka')
    # create_table_doma_dachi_kottedzhi()
    # print(get_item_date_price_area_average_union())
    print(get_item_count_sevastopol_simple('kvartiry_vtorichka'))

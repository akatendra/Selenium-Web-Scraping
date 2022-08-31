import contextlib
import sqlite3


def execute_sql_query_v2(sql):
    with contextlib.closing(sqlite3.connect('avito_database.sqlite',
                                            detect_types=sqlite3.PARSE_DECLTYPES |
                                                         sqlite3.PARSE_COLNAMES
                                            )
                            ) as connection:  # auto-closes
        with connection:  # auto-commits
            with contextlib.closing(
                    connection.cursor()) as cursor:  # auto-closes
                cursor.execute(sql)
        return cursor.fetchall()

def create_connection(db_file):
    # Create a database connection to the SQLite database
    # specified by db_file
    # :param db_file: database file
    # :return: Connection object or None

    connection = None
    try:
        connection = sqlite3.connect(db_file,
                                     detect_types=sqlite3.PARSE_DECLTYPES |
                                     sqlite3.PARSE_COLNAMES
                                     )
        return connection
    except sqlite3.Error as error:
        print('Connection: Error while establish connection to SQLite >>',
              error)

    return connection


def execute_sql_query_v2(sql):
    with contextlib.closing(sqlite3.connect('database.sqlite',
                                            detect_types=sqlite3.PARSE_DECLTYPES |
                                            sqlite3.PARSE_COLNAMES
                                            )
                            ) as connection:  # auto-closes
        with connection:  # auto-commits
            with contextlib.closing(
                    connection.cursor()) as cursor:  # auto-closes
                cursor.execute(sql)
        return cursor.fetchall()


def execute_sql_query(sql):
    with contextlib.closing(sqlite3.connect('database.sqlite',
                                            detect_types=sqlite3.PARSE_DECLTYPES |
                                            sqlite3.PARSE_COLNAMES
                                            )
                            ) as connection, connection, contextlib.closing(
         connection.cursor()) as cursor:
        cursor.execute(sql)
        return cursor.fetchall()


def create_table(connection, create_table_sql):
    # Create a table from the create_table_sql statement
    # :param connection: Connection object
    # :param create_table_sql: a CREATE TABLE statement
    # :return:

    try:
        cursor = connection.cursor()
        print('Create table: Successfully connected to SQLite!')
        cursor.execute(create_table_sql)
    except sqlite3.Error as error:
        print('Create table: Error while making cursor >>', error)
        if connection:
            connection.close()
            print("Create table: SQLite connection is closed after error!")

    # Save (commit) the changes
    connection.commit()
    # Close our connection
    connection.close()
    print('Create table: Table created!')


def create_main_table():
    database = r"database.sqlite"

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
                            item_date TIMESTAMP,
                            item_add_date TIMESTAMP
                            );'''

    # create a database connection
    connection = create_connection(database)

    # create tables
    if connection is not None:
        # create main table
        create_table(connection, sql_create_main_table)
    else:
        print(
            "Create main table: Error! Can't create the database connection.")


def get_item_ids():
    database = r"database.sqlite"
    sql_get_item_ids = 'SELECT item_id FROM items;'

    # create a database connection
    connection = create_connection(database)

    try:
        cursor = connection.cursor()
        print('Get items_id: Successfully connected to SQLite')
        cursor.execute(sql_get_item_ids)
        out_data = cursor.fetchall()
    except sqlite3.Error as error:
        print(error)
        if connection:
            connection.close()
            print("Get items_id: SQLite connection is closed after error!")

    # Save (commit) the changes
    connection.commit()
    # Close our connection
    connection.close()
    print('SQLite: items_ids received!')

    return out_data


def write_to_database(data):
    database = r"database.sqlite"
    items = list(data.values())
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
                    'item_date', 
                    'item_add_date') 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                   '''

    # create a database connection
    connection = create_connection(database)

    try:
        cursor = connection.cursor()

        for item in items:
            data_tuple = tuple((item[item_data] for item_data in item))
            cursor.execute(sql_put_data, data_tuple)
    except sqlite3.Error as error:
        print(error)
        if connection:
            connection.close()
            print("SQLite connection is closed after error")

    # Save (commit) the changes
    connection.commit()
    # Close our connection
    connection.close()
    print('Data saved into database!')


if __name__ == '__main__':
    # create_main_table()
    item_ids = get_item_ids()
    print(type(item_ids), item_ids)

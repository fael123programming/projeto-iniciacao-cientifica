import sqlite3
import os
import hashlib


def stringify_dict(columns: dict):
    res = ''
    size = len(columns.keys())
    for i, key in enumerate(columns.keys()):
        res += str(key) + ' ' + columns[key].upper()
        if i < size - 1:
            res += ', '
    return res


def stringify_list(values: list):
    return str(values).replace('[', '').replace(']', '')


def connect(database='database.db'):
    curr_path = os.path.abspath(__name__).split('utils')[0]
    return sqlite3.connect(os.path.join(curr_path, database))


def create_table(name, columns: dict, replace=True):
    with connect() as conn:
        cursor = conn.cursor()
        if replace:
            try:
                fetch_all_from_table(name)
            except:
                pass
            else:
                cursor.execute(f'DROP TABLE {name}')
        cursor.execute(f'''
            CREATE TABLE {'' if replace else 'IF NOT EXISTS'} {name} ({stringify_dict(columns)});
        ''')
        conn.commit()


def fetch_all_from_table(name):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {name}')
        conn.commit()
        return cursor.fetchall()


def insert_into_table(table_name, values: list):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
            INSERT INTO {table_name} VALUES ({stringify_list(values)});
        ''')
        conn.commit()


def create_dir(name):
    if os.path.exists(name):
        return
    os.mkdir(name)


def generate_hash(row, columns):
    concatenated_data = ''.join(str(row[col]) for col in columns)
    return hashlib.sha256(concatenated_data.encode()).hexdigest()


def columns(table):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table})")
        columns_info = cursor.fetchall()
        column_names = [column[1] for column in columns_info]
        return column_names
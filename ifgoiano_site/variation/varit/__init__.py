from varit import utils
import logging
from datetime import datetime
import os
import pandas as pd
import sqlite3


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.ERROR, format='ERROR: %(asctime)s - %(levelname)s - %(message)s')


def _init():
    utils.create_table('config', {
        'database_name': 'text', 
        'data_dir': 'text', 
        'hashable': 'text', 
        'timestamp': 'text'
    })
    config_rows = config()
    if len(config_rows) == 0:
        data_dir = os.path.abspath(__file__).split('\\__init__.py')[0]
        utils.insert_into_table('config', ['database.db', os.path.join(data_dir, 'data'), '', str(datetime.now())])
        utils.create_dir('data')


def config():
    return utils.fetch_all_from_table('config')


def set_columns(columns: dict):
    columns['hash'] = 'text'
    utils.create_table('data', columns)


def set_data_dir(data_dir):
    with utils.connect() as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
            UPDATE config SET data_dir = '{data_dir}';
        ''')
        conn.commit()


def set_hashable(columns: list):
    cols_str = str(columns).replace('[', '').replace(']', '').replace('\'', '').replace(' ', '')
    with utils.connect() as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
            UPDATE config SET hashable = '{cols_str}';
        ''')
        conn.commit()


def data():
    return utils.fetch_all_from_table('data')


def load():
    config_row = config()[0]
    files = [f for f in os.listdir(config_row[1]) if os.path.isfile(os.path.join(config_row[1], f))]
    columns = [col for col in utils.columns('data') if col in config_row[-2]]
    with utils.connect() as conn:
        for file in files:
            extension = file.split('.')[-1]
            valid_extension = False
            df = None
            if 'csv' in extension:
                df = pd.read_csv(os.path.join(config_row[1], file))
                valid_extension = True

            if 'xls' in extension:
                df = pd.read_excel(os.path.join(config_row[1], file))
                valid_extension = True

            if valid_extension:
                df['hash'] = df.apply(lambda row: utils.generate_hash(row, columns), axis=1)
                df.to_sql('data', conn, if_exists='append', index=False)
            else:
                logging.error(f'Unknown file extension \'{extension}\'')


def variations(columns, timestamp_col, target_col='acessos', time_unit='D'):
    with utils.connect() as conn:
        query = f'SELECT {timestamp_col}, hash, {", ".join(columns)} FROM data'
        df = pd.read_sql_query(query, conn)
        df[timestamp_col] = pd.to_datetime(df[timestamp_col])
        df.set_index(timestamp_col, inplace=True)
        variations_df = df.groupby([timestamp_col, 'hash'])[target_col].apply(lambda x: x.mean())
        variations_df = variations_df.fillna(0)
        variations_df.to_csv('variations.csv')
        return variations_df


def grouped(to_select: list, to_group: list, apply):
    with utils.connect() as conn:
        query = f'SELECT {', '.join(to_select)} FROM data;'
        df = pd.read_sql_query(query, conn)
        # df.set_index('hash', inplace=True)
        group_apply = [item for item in to_select if item not in to_group]
        grouped_df = df.groupby(to_group).apply(lambda x: apply(x[group_apply])).reset_index()
        return grouped_df


_init()
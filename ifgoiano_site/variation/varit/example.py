import os, utils, logging, pandas as pd

def config():
    return utils.fetch_all_from_table('config')

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
                get_hash = lambda row: utils.generate_hash(row, columns)
                df['hash'] = df.apply(get_hash, axis=1)
                df.to_sql('data', conn, if_exists='append', index=False)
            else:
                logging.error(f'Unknown file extension \'{extension}\'')



import pandas as pd
import os


if __name__ == '__main__':
    files = [file for file in os.listdir(os.getcwd()) if file.endswith('.csv')]
    for i, file in enumerate(files):
        df = pd.read_csv(file)
        df['acessos'] = df['acessos'].apply(lambda accesses: accesses - (i + 1))
        df['data_hora'] = pd.to_datetime(df['data_hora'])
        df['data_coleta'] = pd.to_datetime(df['data_coleta'])
        df['acessos_medio_hora'] = df.apply(lambda row: row['acessos'] / ((row['data_coleta'] - row['data_hora']).total_seconds() / 3600), axis=1)
        df.to_csv(file, index=False)
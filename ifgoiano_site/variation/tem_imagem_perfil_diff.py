import sqlite3 as sql
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from tabulate import tabulate

def get_pt_weekday(day):
    return ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo'][day]

if __name__ == '__main__':
    with sql.connect('database.db') as conn:
        query = 'SELECT tem_imagem_perfil, acessos, data_coleta FROM data;'
        df = pd.read_sql_query(query, conn)
        to_group = ['tem_imagem_perfil', 'data_coleta']
        grouped_df = df.groupby(to_group)\
            .apply(lambda x: np.sum(x['acessos']))\
                .reset_index()
        grouped_df.rename(columns={0: 'acessos'}, inplace=True)
        grouped_df['diff_acessos'] = np.nan
        grouped_df['data_coleta'] = pd.to_datetime(grouped_df['data_coleta'])
        cols = grouped_df.columns.tolist()
        vals = grouped_df['tem_imagem_perfil'].unique().tolist()
        for val in vals:
            grouped_local = grouped_df.loc[grouped_df['tem_imagem_perfil'] == val].\
                copy()
            grouped_local.loc[:, 'dia_semana'] = grouped_local['data_coleta'].\
                apply(lambda data_coleta: get_pt_weekday(data_coleta.weekday()))
            grouped_local.loc[:, 'diff_acessos'] = grouped_local['acessos'].diff()
            print(tabulate(grouped_local, headers='keys', tablefmt='psql'))


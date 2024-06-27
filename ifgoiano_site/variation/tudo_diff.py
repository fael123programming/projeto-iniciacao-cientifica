import sqlite3 as sql
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from tabulate import tabulate

def get_pt_weekday(day):
    return ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo'][day]

if __name__ == '__main__':
    with sql.connect('database.db') as conn:
        query = 'SELECT assunto, acessos, data_coleta FROM data;'
        df = pd.read_sql_query(query, conn)
        to_group = ['assunto', 'data_coleta']
        grouped_df = df.groupby(to_group)\
            .apply(lambda x: np.sum(x['acessos']))\
                .reset_index()
        grouped_df.rename(columns={0: 'acessos'}, inplace=True)
        assuntos = grouped_df['assunto'].unique().tolist()
        for assunto in assuntos:
            grouped_local = grouped_df.loc[grouped_df['assunto'] == assunto].copy()
            grouped_local.loc[:, 'data_coleta'] = pd.\
                to_datetime(grouped_local['data_coleta'])
            grouped_local.loc[:, 'dia_semana'] = grouped_local['data_coleta'].\
                apply(lambda data_coleta: get_pt_weekday(data_coleta.weekday()))
            grouped_local.loc[:, 'diff_acessos'] = grouped_local['acessos'].diff()
            print(tabulate(grouped_local, headers='keys', tablefmt='psql'))
        #     plt.plot(grouped_local['data_coleta'], grouped_local['diff_acessos'], marker='o', label=assunto.title())
        #     if assunto == 'campanhas':
        #         for i, row in grouped_local.iterrows():
        #             plt.text(row['data_coleta'], row['diff_acessos'], row['dia_semana'], ha='left', va='bottom', rotation=45)
        # plt.xticks(grouped_df['data_coleta'].unique(), rotation=45, ha='right')
        # plt.ticklabel_format(style='plain', axis='y')
        # plt.xlabel('Data de Coleta')
        # plt.ylabel('Acessos')
        # plt.tight_layout()
        # plt.legend()
        # plt.show()


import sqlite3 as sql
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from tabulate import tabulate

def get_pt_weekday(day):
    return ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo'][day]

if __name__ == '__main__':
    with sql.connect('database.db') as conn:
        query = 'SELECT imagens, acessos, data_coleta FROM data;'
        df = pd.read_sql_query(query, conn)
        to_group = ['imagens', 'data_coleta']
        grouped_df = df.groupby(to_group)\
            .apply(lambda x: np.sum(x['acessos']))\
                .reset_index()
        grouped_df.rename(columns={0: 'acessos'}, inplace=True)
        grouped_df['diff_acessos'] = np.nan
        grouped_df['data_coleta'] = pd.to_datetime(grouped_df['data_coleta'])
        cols = grouped_df.columns.tolist()
        images_count = grouped_df['imagens'].unique().tolist()
        for image_count in images_count:
            grouped_local = grouped_df.loc[grouped_df['imagens'] == image_count].\
                copy()
            grouped_local.loc[:, 'dia_semana'] = grouped_local['data_coleta'].\
                apply(lambda data_coleta: get_pt_weekday(data_coleta.weekday()))
            grouped_local.loc[:, 'diff_acessos'] = grouped_local['acessos'].diff()
            print(tabulate(grouped_local, headers='keys', tablefmt='psql'))
        # print(tabulate(grouped_df, headers='keys', tablefmt='psql'))
        # exit(0)
        # for imgs_count in images_count:
        #     index = df.loc[df['imagens'] == imgs_count].index
        #     df.loc[index[0]:index[-1], cols[-1]] = df.loc[index[0]:index[-1], 'acessos'].diff()
        # df['dia_semana'] = df['data_coleta'].apply(lambda data_coleta: get_pt_weekday(data_coleta.weekday()))
        # max_img_count = max(images_count)
        # for image_count in images_count:
        #     local_df = df[df['imagens'] == image_count]
        #     print(tabulate(local_df, headers='keys', tablefmt='psql'))
    #         plt.plot(local_df['data_coleta'], local_df['diff_acessos'], marker='o', label=f'{image_count} imagem(ns)')
    #         if image_count == max_img_count:
    #             for i, row in local_df.iterrows():
    #                 plt.text(row['data_coleta'], row['diff_acessos'], row['dia_semana'], ha='left', va='bottom', rotation=45)
    #     plt.xticks(df['data_coleta'].unique(), rotation=45, ha='right')
    #     plt.ticklabel_format(style='plain', axis='y')
    #     plt.title('Diferença de Acessos com Tempo')
    #     plt.xlabel('Data de Coleta')
    #     plt.ylabel('Acessos')
    # plt.tight_layout()
    # plt.legend()
    # plt.gcf().set_size_inches(18, 10)
    # plt.savefig('imagens_acessos_diff.png')
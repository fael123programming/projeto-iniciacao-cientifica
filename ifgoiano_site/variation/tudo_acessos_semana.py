import sqlite3 as sql
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from tabulate import tabulate

def get_pt_weekday(day):
    return ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo'][day]

if __name__ == '__main__':
    with sql.connect('./database.db') as conn:
        query = 'SELECT acessos, data_coleta, assunto FROM data'
        df = pd.read_sql(query, conn)
        groupby = ['data_coleta', 'assunto']
        weekday_order = ['domingo', 'segunda', 'terca', \
                         'quarta', 'quinta', 'sexta', 'sabado']
        grouped_df = df.groupby(groupby).sum(numeric_only=True).reset_index()
        grouped_df['dia_semana'] = grouped_df['data_coleta'].\
            apply(lambda x: get_pt_weekday(pd.to_datetime(x).weekday()))
        grouped_df['dia_semana'] = pd.Categorical(grouped_df['dia_semana'], \
        categories=weekday_order, ordered=True)
        assuntos = df['assunto'].unique().tolist()
        weekday_order = ['domingo', 'segunda', 'terca', \
                         'quarta', 'quinta', 'sexta', 'sabado']
        for assunto in assuntos:
            selected_df = grouped_df[grouped_df['assunto'] == assunto].copy()
            selected_df['diff_acessos'] = selected_df['acessos'].diff()
            weekday_grouped = selected_df.loc[:, ['diff_acessos', 'assunto', 'dia_semana']].\
                copy().groupby(['dia_semana', 'assunto'], observed=True).\
                    sum(numeric_only=True).reset_index()
            weekday_grouped.sort_values(by='dia_semana', inplace=True)
            print(tabulate(weekday_grouped, headers='keys', tablefmt='psql'))
            # break
        # df = df[['assunto', 'dia_semana', 'diff_acessos']]
        # df = df.groupby(['assunto', 'dia_semana']).sum().reset_index()


        # plt.figure(figsize=(12, 8))
        # sns.barplot(x='assunto', y='diff_acessos', hue='dia_semana', data=df)
        # plt.title('Variação de Acessos na Semana')
        # plt.xlabel('Assunto')
        # plt.ylabel('Acessos')
        # plt.xticks(rotation=45, ha='right')
        # plt.legend(title='Dia da Semana', bbox_to_anchor=(1.05, 1), loc='upper left')
        # plt.tight_layout()
        # plt.savefig('tudo_acessos_semana.png')
        # plt.show()
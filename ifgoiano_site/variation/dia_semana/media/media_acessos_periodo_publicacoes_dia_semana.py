import sqlite3 as sql
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def get_pt_weekday(day):
    return ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo'][day]

if __name__ == '__main__':
    with sql.connect('database.db') as conn:
        query = 'SELECT acessos, data_coleta FROM data;'
        df = pd.read_sql_query(query, conn)
        to_group = ['data_coleta']
        grouped_df = df.groupby(to_group).apply(lambda x: np.sum(x['acessos'])).reset_index()
        grouped_df.rename(columns={0: 'acessos'}, inplace=True)
        grouped_df['acessos'] = grouped_df['acessos'].diff()
        grouped_df['data_coleta'] = pd.to_datetime(grouped_df['data_coleta'])
        grouped_df['dia_semana'] = grouped_df['data_coleta'].apply(lambda data_coleta: get_pt_weekday(data_coleta.weekday()))
        data_df = grouped_df[['dia_semana', 'acessos']].groupby('dia_semana').mean().reset_index()
        data_df['acessos'] = data_df['acessos'].astype(int)
        ordem_dias_semana = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado']
        data_df['dia_semana'] = pd.Categorical(data_df['dia_semana'], categories=ordem_dias_semana, ordered=True)
        data_df = data_df.sort_values(by='dia_semana')
        fig, ax = plt.subplots(figsize=(10, 5), layout='constrained')
        ax.bar(data_df['dia_semana'].apply(lambda x: x.title()), data_df['acessos'])
        x = data_df['dia_semana'].values.tolist()
        y = data_df['acessos'].values.tolist()
        for i, v in enumerate(y):
            plt.text(i, v, str(v), ha='center')
        plt.title('Média de Acessos por Dia da Semana')
        plt.xlabel('Assunto')
        plt.ylabel('Média de Acessos')
        plt.show()


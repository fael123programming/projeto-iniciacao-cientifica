import sqlite3 as sql
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

if __name__ == '__main__':
    with sql.connect('database.db') as conn:
        query = 'SELECT assunto, acessos, data_coleta FROM data;'
        df = pd.read_sql_query(query, conn)
        to_group = ['assunto', 'data_coleta']
        grouped_df = df.groupby(to_group).apply(lambda x: np.sum(x['acessos'])).reset_index()
        grouped_df.rename(columns={0: 'acessos'}, inplace=True)
        assuntos = grouped_df['assunto'].unique().tolist()
        data = dict(assunto=list(), acessos=list())
        for assunto in assuntos:
            grouped_local = grouped_df.loc[grouped_df['assunto'] == assunto].copy()
            data['assunto'].append(assunto)
            data['acessos'].append(int(sum(grouped_local['acessos'].diff().tolist()[1:])))
        data_df = pd.DataFrame(data)
        fig, ax = plt.subplots(figsize=(10, 5), layout='constrained')
        ax.bar(data_df['assunto'].apply(lambda x: x.title()), data_df['acessos'])
        x = data_df['assunto'].values.tolist()
        y = data_df['acessos'].values.tolist()
        for i, v in enumerate(y):
            plt.text(i, v, str(v), ha='center')
        plt.title('Quantidade de Acessos por Assunto')
        plt.xlabel('Assunto')
        plt.ylabel('Qtd. de Acessos')
        # plt.show()
        plt.savefig('soma_acessos_periodo_publicacoes_assunto.png')


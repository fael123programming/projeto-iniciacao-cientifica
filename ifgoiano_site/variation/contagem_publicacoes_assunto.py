import pandas as pd
import sqlite3 as sql
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker


if __name__ == '__main__':
    with sql.connect('varit/database.db') as conn:
        df = pd.read_sql_query(sql='''
            SELECT assunto, count(*) as noticias FROM data group by assunto;
        ''', con=conn)
        fig, ax = plt.subplots(figsize=(10, 5), layout='constrained')
        ax.bar(df['assunto'].apply(lambda assunto: assunto.title()), df['noticias'])
        x = df['assunto'].values.tolist()
        y = df['noticias'].values.tolist()
        for i, v in enumerate(y):
            plt.text(i, v, str(v), ha='center')
        plt.title('Quantidade de Publicações por Assunto')
        plt.xlabel('Assunto')
        plt.ylabel('Qtd. Notícias')
        # plt.show()
        plt.savefig('contagem_publicacoes_assunto.png')
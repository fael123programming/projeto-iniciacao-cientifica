import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

if __name__ == '__main__':
    df = pd.read_csv(
        'datasets/pubs_data_sentiment_2024_03_21_18_05_15_1_19_42.csv')
    mean_descricao_estrelas = round(
        np.mean(df['descricao_estrelas'].values.tolist()), 2)
    mean_descricao_pontuacao = round(
        np.mean(df['descricao_pontuacao'].values.tolist()), 2)
    mean_corpo_summ_estrelas = round(
        np.mean(df['corpo_summ_estrelas'].values.tolist()), 2)
    mean_corpo_summ_pontuacao = round(
        np.mean(df['corpo_summ_pontuacao'].values.tolist()), 2)
    x_plt1 = ['Descrição do jornalista', 'Descrição do modelo BART']
    y_plt1 = [mean_descricao_estrelas, mean_corpo_summ_estrelas]
    plt.bar(
        x_plt1,
        y_plt1,
        color='blue',
        # width=.4
    )
    for x, y in zip(x_plt1, y_plt1):
        plt.annotate(
            (str(y) + '0')[0:str(y).index('.') + 3], 
            (x, y), 
            textcoords='offset points', 
            xytext=(0, 3), 
            ha='center'
        )
    plt.xlabel('Origem do Texto')
    plt.ylabel('Média de Estrelas')
    plt.title('Média de Estrelas Obtida por cada Tipo de Texto')
    plt.savefig('charts/media_estrelas.png')
    plt.clf()
    x_plt2 = ['Descrição do jornalista', 'Descrição do modelo BART']
    y_plt2 = [mean_descricao_pontuacao, mean_corpo_summ_pontuacao]
    plt.bar(
        x_plt2,
        y_plt2,
        color='blue',
        width=.4
    )
    for x, y in zip(x_plt2, y_plt2):
        plt.annotate(
            (str(y) + '0')[0:str(y).index('.') + 3], 
            (x, y), 
            textcoords='offset points', 
            xytext=(0, 3), 
            ha='center'
        )
    plt.xlabel('Origem do Texto')
    plt.ylabel('Média da Pontuação')
    plt.title('Média da Pontuação Obtida por cada Tipo de Texto')
    plt.savefig('charts/media_pontuacao.png')
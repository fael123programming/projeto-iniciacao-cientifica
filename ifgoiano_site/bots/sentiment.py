import pandas as pd
import numpy as np
from transformers import pipeline

sentiment_analyser = pipeline(
    'sentiment-analysis', 
    model='nlptown/bert-base-multilingual-uncased-sentiment'
)

if __name__ == '__main__':
    df = pd.read_csv('./datasets/pubs_data_summarized_2024_03_21_18_05_15_1_19_42.csv')
    df.dropna(how='any', axis=0, inplace=True)
    df.reset_index(inplace=True)
    df.drop(columns=['index'], inplace=True)
    df['descricao_estrelas'] = pd.NA
    df['descricao_pontuacao'] = pd.NA
    df['corpo_summ_estrelas'] = pd.NA
    df['corpo_summ_pontuacao'] = pd.NA
    for i in range(df.shape[0]):
        try:
            sentimento_descricao = sentiment_analyser(
                df.loc[i, 'descricao']
            )[0]
        except:
            df.drop(i, inplace=True)
        else:
            df.loc[i, 'descricao_estrelas'] = int(sentimento_descricao['label'].split()[0])
            df.loc[i, 'descricao_pontuacao'] = sentimento_descricao['score']
            sentimento_corpo_summ = sentiment_analyser(
                df.loc[i, 'corpo_summ']
            )[0]
            df.loc[i, 'corpo_summ_estrelas'] = int(sentimento_corpo_summ['label'].split()[0])
            df.loc[i, 'corpo_summ_pontuacao'] = sentimento_corpo_summ['score']
            print(f'({i}) done')
    df.reset_index(inplace=True)
    df.drop(columns=['index'], inplace=True)
    df.to_csv('datasets/pubs_data_sentiment_2024_03_21_18_05_15_1_19_42.csv', index=False)
import pandas as pd
import numpy as np
from transformers import pipeline, \
    BartForConditionalGeneration, BartTokenizer

MODEL = 'facebook/bart-large-cnn'

summarizer = pipeline('summarization', model=MODEL)
tokenizer = BartTokenizer.from_pretrained(MODEL)
model = BartForConditionalGeneration.from_pretrained(MODEL)

if __name__ == '__main__':
    df = pd.read_csv(\
        'datasets/pubs_data_2024_03_21_18_05_15_1_19_42.csv')  # Leitura do dataset.
    df = df.dropna(how='any', axis=0).reset_index()
    df = df.drop(columns=['index']) # Limpeza de dados.
    desc_list = df['descricao'].values.tolist()
    # Cálculo do comprimento máximo, mínimo e médio das descrições.
    max_size = max(list(map(lambda desc: len(desc), desc_list)))
    min_size = min(list(map(lambda desc: len(desc), desc_list)))
    descricao_mean_size = int(sum(list(map(lambda desc: len(desc), \
        desc_list))) / len(desc_list) + .5)
    # Cálculo do desvio padrão do comprimento das descrições.
    descricao_stddev_size = int(np.std(list(map(lambda desc: \
        len(desc), desc_list))) + .5)
    # Cálculo no comprimento máximo e mínimo da sumarização. 
    min_size_summarization = (lambda val: 0 if val < 0 else \
        val)(descricao_mean_size - descricao_stddev_size)
    max_size_summarization = descricao_mean_size + \
        descricao_stddev_size
    df['corpo_summ'] = ''
    # Realizar sumarização dos corpos das notícias.
    for i in range(df.shape[0]):
        inputs = tokenizer( # Divisão do texto em tokens.
            df.loc[i, 'corpo'],
            max_length=1024,
            return_tensors='pt',
            padding=True,
            truncation=True
        )
        summary_ids = model.generate( # IDentificação dos tokens.
            inputs['input_ids'],
            num_beams=4,
            min_length=min_size_summarization,
            max_length=max_size_summarization,
            early_stopping=True
        )
        decoded = tokenizer.decode( # Decodificação dos tokens.
            summary_ids[0],
            skip_special_tokens=True
        )
        summary_text = summarizer( # Sumarizador com modelo BART.
            decoded,
            do_sample=False
        )[0]['summary_text']
        df.loc[i, 'corpo_summ'] = summary_text
        print(f'({i + 1}) done')
    # df.to_csv('datasets/pubs_data_summarized_2024_03_21_18_05_15_1_19_42.csv', index=False)

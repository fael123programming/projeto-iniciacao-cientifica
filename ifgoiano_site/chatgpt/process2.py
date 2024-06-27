import os, pandas, time, openai, decouple
from classify import get_messages, DICIO_REJANE
from process import EXPORT_ARGS

openai.api_key = decouple.config('TEST_KEY')

PATH = 'C:/Users/Rafae/OneDrive/Documentos/projeto_iniciacao_cientifica/ifgoiano_site/datasets/class/pubs_data_2023_02_13_23_22_05_4_05_04.csv'

if __name__ == '__main__':
    df = pandas.read_csv(PATH)
    for i in range(df.shape[0]):
        if df.loc[i, 'assunto'] == '-':
            title, desc = df.loc[i, ['titulo', 'descricao']]
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=get_messages(title, desc)
            )
            ans = response['choices'][0]['message']['content'].strip().replace('.', '')
            print(ans)
            df.loc[i, 'assunto'] = ans
            time.sleep(20)
    df.to_csv(PATH, **EXPORT_ARGS)
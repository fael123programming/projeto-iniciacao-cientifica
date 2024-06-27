import os, pandas

SOURCE_PATH = 'C:\\Users\\Rafae\\OneDrive\\Documentos\\projeto_iniciacao_cientifica\\ifgoiano_site\\datasets\\class'

EXPORT_ARGS = dict(encoding='utf-8', index=False)

if __name__ == '__main__':
    df1 = pandas.read_csv('C:\\Users\\Rafae\\OneDrive\\Documentos\\projeto_iniciacao_cientifica\\ifgoiano_site\\datasets\\clean\\pubs_data_2023_02_13_23_22_05_4_05_04.csv')
    df2 = pandas.read_csv("C:/Users/Rafae/OneDrive/Documentos/projeto_iniciacao_cientifica/ifgoiano_site/datasets/class/pubs_data_2023_02_04_21_36_49_4_24_20.csv")
    df1['assunto'] = '-';
    df2['assunto'] = df2['subject']
    df2 = df2.drop(columns=['subject'])
    diff = df1.shape[0] - df2.shape[0]
    
    for i in range(diff, df1.shape[0]):
        title2, desc2 = df2.loc[i - diff, ['titulo', 'descricao']]
        title1, desc1 = df1.loc[i, ['titulo', 'descricao']]
        if title1 != title2 and desc1 != desc2:
            print(f'FOUND: {i - diff} and {i}')
            print(f'title1={title1}')
            print(f'title2={title2}')
            print(f'desc1={desc1}')
            print(f'desc2={desc2}')
        else:
            df1.loc[i, 'assunto'] = df2.loc[i - diff, 'assunto']
    df1.to_csv('C:/Users/Rafae/OneDrive/Documentos/projeto_iniciacao_cientifica/ifgoiano_site/datasets/class/pubs_data_2023_02_13_23_22_05_4_05_04.csv', **EXPORT_ARGS)
    df2.to_csv("C:/Users/Rafae/OneDrive/Documentos/projeto_iniciacao_cientifica/ifgoiano_site/datasets/class/pubs_data_2023_02_04_21_36_49_4_24_20.csv", **EXPORT_ARGS)
    # files = os.listdir(SOURCE_PATH)
    # for f in files:
        # df = pandas.read_csv(os.path.join(SOURCE_PATH, f))
        # print('rows=', df.shape[0])
        
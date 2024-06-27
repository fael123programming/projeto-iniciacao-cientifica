import pandas as pd


if __name__ == '__main__':
    df = pd.read_csv('pubs_data_2023_02_13_23_22_05_4_05_04.csv')
    df['text'] = df['titulo'] + ' ' + df['descricao']
    df = df.drop(columns=['titulo', 'descricao', 'data_hora', 'dia_semana', 'periodo_dia', 'imagens', 'acessos', 'acessos_medio_hora', 'tem_imagem_perfil', 'assunto'], axis=1)
    df.to_csv('pubs_text_2023_02_13_23_22_05_4_05_04.csv', index=False, encoding='utf-8')

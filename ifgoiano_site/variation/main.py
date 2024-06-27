from varit import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter
import seaborn as sns


def get_pt_weekday(day):
    return ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo'][day]


if __name__ == '__main__':
    pass  

    # set_data_dir('C:/Users/Rafae/OneDrive/Documentos/projeto_iniciacao_cientifica/ifgoiano_site/datasets/class')
    # set_hashable(['titulo', 'descricao', 'data_hora'])
    # set_columns({
    #     'titulo': 'text',
    #     'descricao': 'text',
    #     'data_hora': 'text',
    #     'dia_semana': 'text',
    #     'periodo_dia': 'text',
    #     'imagens': 'integer',
    #     'acessos': 'integer',
    #     'acessos_medio_hora': 'real',
    #     'tem_imagem_perfil': 'text',
    #     'assunto': 'text',
    #     'data_coleta': 'text',
    #     'estrelas_bert': 'integer',
    #     'pontuacao_bert': 'real'
    # })
    # load()
    # df = grouped(['tem_imagem_perfil', 'acessos'], ['tem_imagem_perfil'], np.sum)
    # print(df)
    # exit(0)
    # df = grouped(['tem_imagem_perfil', 'data_coleta', 'acessos'], ['tem_imagem_perfil', 'data_coleta'], np.sum)
    # df['data_coleta'] = pd.to_datetime(df['data_coleta'])
    # df['diff_acessos'] = np.nan
    # cols = df.columns.tolist()
    # tem_opt = df['tem_imagem_perfil'].unique().tolist()
    # for opt in tem_opt:
    #     index = df.loc[df['tem_imagem_perfil'] == opt].index
    #     df.loc[index[0]:index[-1], cols[-1]] = df.loc[index[0]:index[-1], 'acessos'].diff()
    # tem_opts = df['tem_imagem_perfil'].unique().tolist()
    # img_text = {
    #     'nao': 'Não possui imagem de perfil',
    #     'sim': 'Possui imagem de perfil'
    # }
    # for tem_opt in tem_opts[::-1]:
    #     local_df = df[df['tem_imagem_perfil'] == tem_opt]
    #     plt.plot(local_df['data_coleta'], local_df['diff_acessos'], marker='o', label=img_text[tem_opt])
    # plt.xticks(df['data_coleta'].unique(), rotation=45, ha='right')
    # plt.ticklabel_format(style='plain', axis='y')
    # plt.tight_layout()
    # plt.gcf().set_size_inches(18, 10)
    # plt.legend()
    # plt.xlabel('Data de Coleta')
    # plt.ylabel('Acessos')
    # plt.title('Diferença de Acessos com Tempo')
    # plt.savefig('tem_imagem_perfil_acessos.png')
    # plt.figure(figsize=(12, 8))
    # sns.barplot(x='tem_imagem_perfil', y='diff_acessos', hue='dia_semana', data=df)
    # plt.title('Variação de Acessos na Semana')
    # plt.xlabel('Notícia Tem Imagem de Perfil')
    # plt.ylabel('Acessos')
    # plt.xticks(rotation=0, ha='right')
    # plt.legend(title='Dia da Semana', bbox_to_anchor=(1.05, 1), loc='upper left')
    # plt.tight_layout()
    # df = grouped(['tem_imagem_perfil', 'data_coleta', 'acessos'], ['tem_imagem_perfil', 'data_coleta'], np.sum)
    # df['data_coleta'] = pd.to_datetime(df['data_coleta'])
    # df['diff_acessos'] = np.nan
    # cols = df.columns.tolist()
    # tem_opt = df['tem_imagem_perfil'].unique().tolist()
    # for opt in tem_opt:
    #     index = df.loc[df['tem_imagem_perfil'] == opt].index
    #     df.loc[index[0]:index[-1], cols[-1]] = df.loc[index[0]:index[-1], 'acessos'].diff()
    # df['dia_semana'] = df['data_coleta'].apply(lambda data_coleta: get_pt_weekday(data_coleta.weekday()))
    # df = df[['tem_imagem_perfil', 'diff_acessos', 'dia_semana']].groupby(['tem_imagem_perfil', 'dia_semana']).sum().reset_index()
    # weekday_order = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado']
    # df['dia_semana'] = pd.Categorical(df['dia_semana'], categories=weekday_order, ordered=True)
    # df = df.sort_values(by='dia_semana')
    # plt.figure(figsize=(12, 8))
    # sns.barplot(x='tem_imagem_perfil', y='diff_acessos', hue='dia_semana', data=df)
    # plt.title('Variação de Acessos na Semana')
    # plt.xlabel('Notícia Tem Imagem de Perfil')
    # plt.ylabel('Acessos')
    # plt.xticks(rotation=0, ha='right')
    # plt.legend(title='Dia da Semana', bbox_to_anchor=(1.05, 1), loc='upper left')
    # plt.tight_layout()
    # plt.show()
    # plt.savefig('tem_imagem_perfil_acessos_semana_diff.png')
    # df = grouped(['imagens', 'data_coleta', 'acessos'], ['imagens', 'data_coleta'], np.sum)
    # df['data_coleta'] = pd.to_datetime(df['data_coleta'])
    # df['diff_acessos'] = np.nan
    # cols = df.columns.tolist()
    # images_count = df['imagens'].unique().tolist()
    # for imgs_count in images_count:
    #     index = df.loc[df['imagens'] == imgs_count].index
    #     df.loc[index[0]:index[-1], cols[-1]] = df.loc[index[0]:index[-1], 'acessos'].diff()
    # df['dia_semana'] = df['data_coleta'].apply(lambda data_coleta: get_pt_weekday(data_coleta.weekday()))
    # df = df[['imagens', 'diff_acessos', 'dia_semana']].groupby(['imagens', 'dia_semana']).sum().reset_index()
    # weekday_order = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado']
    # df['dia_semana'] = pd.Categorical(df['dia_semana'], categories=weekday_order, ordered=True)
    # df = df.sort_values(by='dia_semana')

    # plt.figure(figsize=(12, 8))
    # sns.barplot(x='imagens', y='diff_acessos', hue='dia_semana', data=df)
    # plt.title('Variação de Acessos na Semana')
    # plt.xlabel('Qtd. de Imagens na Notícia')
    # plt.ylabel('Acessos')
    # plt.xticks(rotation=0, ha='right')
    # plt.legend(title='Dia da Semana', bbox_to_anchor=(1.05, 1), loc='upper left')
    # plt.tight_layout()
    # plt.savefig('imagens_acessos_semana_diff.png')

    # df = grouped(['imagens', 'data_coleta', 'acessos'], ['imagens', 'data_coleta'], np.sum)
    # df['diff_acessos'] = np.nan
    # df['data_coleta'] = pd.to_datetime(df['data_coleta'])
    # cols = df.columns.tolist()
    # images_count = df['imagens'].unique().tolist()
    # for imgs_count in images_count:
    #     index = df.loc[df['imagens'] == imgs_count].index
    #     df.loc[index[0]:index[-1], cols[-1]] = df.loc[index[0]:index[-1], 'acessos'].diff()
    # df['dia_semana'] = df['data_coleta'].apply(lambda data_coleta: get_pt_weekday(data_coleta.weekday()))
    # max_img_count = max(images_count)
    # for image_count in images_count:
    #     local_df = df[df['imagens'] == image_count]
    #     plt.plot(local_df['data_coleta'], local_df['diff_acessos'], marker='o', label=f'{image_count} imagem(ns)')
    #     if image_count == max_img_count:
    #         for i, row in local_df.iterrows():
    #             plt.text(row['data_coleta'], row['diff_acessos'], row['dia_semana'], ha='left', va='bottom', rotation=45)
    # plt.xticks(df['data_coleta'].unique(), rotation=45, ha='right')
    # plt.ticklabel_format(style='plain', axis='y')
    # plt.title('Diferença de Acessos com Tempo')
    # plt.xlabel('Data de Coleta')
    # plt.ylabel('Acessos')
    # plt.tight_layout()
    # plt.legend()
    # plt.gcf().set_size_inches(18, 10)
    # plt.savefig('imagens_acessos_diff.png')
    # df = grouped(['assunto', 'data_coleta', 'acessos'], ['assunto', 'data_coleta'], np.sum)
    # df['data_coleta'] = pd.to_datetime(df['data_coleta'])
    # assuntos = df['assunto'].unique().tolist()
    # for assunto in assuntos:
    #     local_df = df[df['assunto'] == assunto]
    #     plt.plot(local_df['data_coleta'], local_df['acessos'])
    #     plt.scatter(local_df['data_coleta'], local_df['acessos'], color='blue', zorder=3)
    #     for x, y in zip(local_df['data_coleta'], local_df['acessos']):
    #         plt.annotate(f'{get_pt_weekday(x.weekday())}', (x, y), textcoords="offset points", xytext=(-10, 10), ha='center')
        # for x, y in zip(local_df['data_coleta'], local_df['acessos']):
        #     plt.annotate(f'{y}', (x, y), textcoords="offset points", xytext=(-10, 10), ha='center')
        # plt.xticks(rotation=45, ha='right')
        # plt.xlabel('Data da Coleta')
        # plt.ylabel('Acessos')
        # plt.title(f'Acessos Totais de Notícias Sobre {assunto.title()} Durante Coleta')
        # plt.tick_params(axis='y', labelcolor='tab:blue')
        # plt.gca().get_yaxis().get_major_formatter().set_scientific(False)
        # plt.subplots_adjust(left=.15, bottom=.25)
        # plt.show()
        # plt.tight_layout()
        # plt.gcf().set_size_inches(18, 10)
        # plt.savefig('tudo_' + assunto.lower().replace(' ', '_') + '.png', bbox_inches='tight')
        # plt.clf()
        # break
    # print(df)
    # df = grouped(['assunto', 'data_coleta', 'acessos'], ['assunto', 'data_coleta'], np.sum)
    # df['diff_acessos'] = np.nan
    # cols = df.columns.tolist()
    # assuntos = df['assunto'].tolist()
    # assunto_col_index = cols.index('assunto')
    # acesses_col_index = cols.index('acessos')
    # for assunto in assuntos:
    #     index = df.loc[df['assunto'] == assunto].index
    #     df.loc[index[0]:index[-1], cols[-1]] = df.loc[index[0]:index[-1], 'acessos'].diff()

    # df = df[['assunto', 'diff_acessos']].groupby('assunto').sum().reset_index()
    # with sqlite3.connect('./varit/database.db') as conn:
    #     count = pd.read_sql_query('SELECT * FROM data', conn)
    #     hashes = count[['assunto', 'hash']].groupby('assunto').count().reset_index()['hash'].tolist()
    
    # df['diff_acessos'] = df['diff_acessos'] / hashes
    # df1 = grouped(['assunto', 'estrelas_bert'], ['assunto'], np.mean)
    # df2 = grouped(['assunto', 'pontuacao_bert'], ['assunto'], np.mean)
    # df['estrelas_bert'] = df1[0]
    # df['pontuacao_bert'] = df2[0]

    # fig, ax1 = plt.subplots(figsize=(10, 6))

    # color = 'tab:blue'
    # ax1.set_xlabel('Assunto')
    # ax1.set_ylabel('Media Acessos por Dia', color=color)
    # ax1.bar(df['assunto'], df['diff_acessos'], color=color)
    # ax1.tick_params(axis='y', labelcolor=color)

    # Plot Estrelas BERT
    # ax2 = ax1.twinx()  
    # color = 'black'
    # ax2.set_ylabel('Estrelas BERT', color=color)  
    # ax2.plot(df['assunto'], df['estrelas_bert'], color=color)
    # ax2.scatter(df['assunto'], df['estrelas_bert'], color=color)  # Add scatter plot
    # ax2.tick_params(axis='y', labelcolor=color)

    # Plot Pontuacao BERT
    # ax3 = ax1.twinx()  
    # color = 'tab:red'
    # ax3.spines['right'].set_position(('outward', 60))  
    # ax3.set_ylabel('Pontuacao BERT', color=color)
    # ax3.plot(df['assunto'], df['pontuacao_bert'], color=color)
    # ax3.scatter(df['assunto'], df['pontuacao_bert'], color=color)  # Add scatter plot
    # ax3.tick_params(axis='y', labelcolor=color)

    # fig.tight_layout()  
    # plt.title('QTD. Acessos / Estrelas e Pontuação BERT')
    # plt.gcf().set_size_inches(9, 5)
    # plt.savefig('bert_mean_new2.png')
    # plt.show()  # Add this line to display the plot
    # df['dia_semana'] = df['data_coleta'].apply(lambda x: get_pt_weekday(x.weekday()))
    # df = df[['assunto', 'dia_semana', 'diff_acessos']]
    
    # df = df.groupby(['assunto', 'dia_semana']).sum().reset_index()

    # weekday_order = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado']
    # df['dia_semana'] = pd.Categorical(df['dia_semana'], categories=weekday_order, ordered=True)
    # df = df.sort_values(by='dia_semana')

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
    # plt.figure(figsize=(10, 6))
    # plt.title('Diferença de Acessos na Semana')
    # plt.xlabel('Dia da Semana')
    # plt.ylabel('Acessos')

    # for assunto in assuntos:
    #     grouped_local = grouped_df[grouped_df['assunto'] == assunto]
    #     grouped_local['data_coleta'] = pd.to_datetime(grouped_local['data_coleta'])
    #     grouped_local['dia_semana'] = grouped_local['data_coleta'].apply(lambda data_coleta: get_pt_weekday(data_coleta.weekday()))
    #     grouped_local['diff_acessos'] = grouped_local['acessos'].diff()

    #     plt.plot(grouped_local['data_coleta'], grouped_local['diff_acessos'], marker='o', label=assunto.title())

    #     if assunto == 'campanhas':
    #         for i, row in grouped_local.iterrows():
    #             plt.text(row['data_coleta'], row['diff_acessos'], row['dia_semana'], ha='left', va='bottom', rotation=45)

    # Set x-axis ticks once for the entire plot
    # plt.xticks(grouped_df['data_coleta'].unique(), rotation=45, ha='right')

    # Prevent y-axis labels from being displayed in scientific notation
    # plt.ticklabel_format(style='plain', axis='y')

    # plt.tight_layout()
    # plt.legend()
    # plt.savefig('tudo_diff.png')
    # plt.show()


    #     plt.figure(figsize=(10, 6))
    #     plt.plot(grouped_local['data_coleta'], grouped_local['diff_acessos'], marker='o', label='acessos')
    #     plt.title(f'{assunto.title()}: Diferença de Acessos com Tempo')
    #     plt.xlabel('Data de Coleta')
    #     plt.ylabel('Diferença de Acessos')
    #     plt.xticks(grouped_local['data_coleta'], rotation=45, ha='right')
    #     plt.legend()

    #     for i, row in grouped_local.iterrows():
    #         plt.text(row['data_coleta'], row['diff_acessos'], row['dia_semana'], ha='left', va='bottom')

    #     plt.tight_layout()
    #     plt.savefig(os.path.join(path, 'diff.png'))

    #     plt.clf()


    # grouped_df['diff_acessos'] = grouped_df.groupby(['data_coleta', 'assunto'])['acessos'].diff(1)
    # print(grouped_df[grouped_df['hash'] == '0012e94c173887da0d3583a5f3b0015d47f3932be6258631ebfc6bd617e64f3e'])
    # print(utils.fetch_all_from_table('data')[0])
    # print(variations(['acessos'], 'data_hora'))
    # Exemplo de uso
    # selected_columns_to_monitor = ['coluna1', 'coluna2']  # Substitua com as colunas desejadas
    # time_unit_to_monitor = 'days'  # Pode ser 'hours', 'minutes', etc.

    # result = calculate_variations(selected_columns_to_monitor, time_unit_to_monitor)
    # print(result)

    # # Exemplo de uso
    # file_path = 'seu_arquivo.csv'
    # selected_columns = ['coluna1', 'coluna2']  # Substitua com as colunas desejadas

    # load_data(file_path, selected_columns)
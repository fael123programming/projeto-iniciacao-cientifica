import pandas as pd
import os
import numpy as nm
import util


def datetime_to_plain_text(datetime_obj):
    return str(datetime_obj).split('.')[0].replace(' ', '_').replace('-', '_').replace(':', '_').replace('.', '_')


def get_weekday(timestamp):
    if timestamp is None:
        return "desconhecido"
    weekday = timestamp.weekday()
    if weekday == 0:
        return "segunda"
    elif weekday == 1:
        return "terca"
    elif weekday == 2:
        return "quarta"
    elif weekday == 3:
        return "quinta"
    elif weekday == 4:
        return "sexta"
    elif weekday == 5:
        return "sabado"
    elif weekday == 6:
        return "domingo"
    else:
        return "desconhecido"


def pubs_data_are_equal(pub_data1, pub_data2):
    return pub_data1['titulo'] == pub_data2['titulo'] and pub_data1['data_hora'] == pub_data2['data_hora']


def print_pub_data(data, dataset_name):
    print('Processing...')
    print('-' * 100)
    print('|', f'Dataset: {dataset_name}'.center(98), sep='', end='|\n')
    print('|', f'Title: {data["titulo"][:50]}...'.center(98), sep='', end='|\n')
    print('|', f'Descricao: {data["descricao"][:50]}...'.center(98), sep='', end='|\n')
    print('|', f'Data/hora: {data["data_hora"]}'.center(98), sep='', end='|\n')
    print('-' * 100)


def header():
    print('-' * 119)
    print('|', f'{"Source dataset":<50}{"Target dataset":<50}{"Total":<15}', '|')
    print('-' * 119)


def status(log_list):
    for log in log_list:
        print('|', f'{log["source_dataset"]:<50}{log["target_dataset"]:<50}'
                   f'{str(log["already_done"]) + "/" + str(log["total"]):<15}', '|')


def clear_cmd():
    os.system('cls' if os.name == 'nt' else 'clear')


def create_datasets_with_id_column():
    datasets = util.get_datasets()
    for dataset in datasets:
        dt = pd.read_csv(f'../datasets/raw/{dataset}')
        id_ = 100000
        for i in range(len(dt) - 1, -1, -1):
            dt.loc[i, 'id'] = id_
            id_ += 1
        dt['id'] = dt['id'].astype(nm.int64)
        dt.to_csv(f'/home/leafar/new_datasets/{dataset}', index=False)


def clean_datasets():
    datasets = util.get_datasets()
    for dt in datasets:
        df = util.read_dataset(dt)
        print(util.PATH_RAW_DATASETS + dt)
        df.to_csv(util.PATH_RAW_DATASETS + dt, index=False)


def generate_reports():
    data_dict = dict(
        data_hora_ant=list(),
        data_hora_dep=list(),
        dia_semana_ant=list(),
        dia_semana_dep=list(),
        acessos_inter=list(),
        acessos_medio_hora_inter=list(),
        acessos_geral=list(),
        acessos_medio_hora_geral=list(),
        titulo=list(),
        descricao=list(),
        data_hora_pub=list(),
        dia_semana_pub=list(),
        periodo_dia_pub=list(),
        imagens=list(),
        tem_imagem_perfil=list()
    )
    datasets = util.get_datasets()
    datasets_run = datasets[:len(datasets) - 1]
    logs = list()
    len_datasets_run = len(datasets_run)
    for i in range(len_datasets_run):  # Run through all datasets least the last one.
        dt = util.read_dataset(datasets_run[i])  # Read the current dataset based on 'i'.
        next_dt = util.read_dataset(datasets[i + 1])  # Read the next dataset.
        data_hora_ant = util.get_execution_datetime(datasets_run[i])
        data_hora_dep = util.get_execution_datetime(datasets[i + 1])
        len_dt, len_next_dt = len(dt), len(next_dt)
        logs.append(
            {
                'source_dataset': datasets_run[i],
                'target_dataset': datasets[i + 1],
                'already_done': 0,
                'total': len_dt
            }
        )
        for j in range(len_dt):  # Run through each line of the current dataset.
            header()
            status(logs)
            current_pub_values = dt.loc[j, ['titulo', 'descricao', 'data_hora', 'acessos']]
            g = len_next_dt - len_dt + j
            while g < len_next_dt:
                current_pub_values_nxt_dt = next_dt.loc[
                    g,
                    ['titulo', 'descricao', 'data_hora', 'acessos', 'acessos_medio_hora', 'dia_semana',
                     'periodo_dia', 'imagens', 'tem_imagem_perfil']
                ]
                if pubs_data_are_equal(
                        current_pub_values[['titulo', 'data_hora']],
                        current_pub_values_nxt_dt[['titulo', 'data_hora']]
                ):
                    data_dict['data_hora_ant'].append(data_hora_ant)
                    data_dict['data_hora_dep'].append(data_hora_dep)
                    data_dict['dia_semana_ant'].append(get_weekday(data_hora_ant))
                    data_dict['dia_semana_dep'].append(get_weekday(data_hora_dep))
                    acessos_inter = current_pub_values_nxt_dt['acessos'] - current_pub_values['acessos']
                    data_dict['acessos_inter'].append(acessos_inter)
                    hours_inter = (data_hora_dep - data_hora_ant).total_seconds() / 3600
                    data_dict['acessos_medio_hora_inter'].append(round(acessos_inter / hours_inter, 2))
                    data_dict['acessos_geral'].append(current_pub_values_nxt_dt['acessos'])
                    data_dict['acessos_medio_hora_geral'].append(current_pub_values_nxt_dt['acessos_medio_hora'])
                    data_dict['titulo'].append(current_pub_values_nxt_dt['titulo'])
                    data_dict['descricao'].append(current_pub_values_nxt_dt['descricao'])
                    data_dict['data_hora_pub'].append(current_pub_values_nxt_dt['data_hora'])
                    data_dict['dia_semana_pub'].append(current_pub_values_nxt_dt['dia_semana'])
                    data_dict['periodo_dia_pub'].append(current_pub_values_nxt_dt['periodo_dia'])
                    data_dict['imagens'].append(current_pub_values_nxt_dt['imagens'])
                    data_dict['tem_imagem_perfil'].append(current_pub_values_nxt_dt['tem_imagem_perfil'])
                    break
                g += 1
            # clear_cmd()
            # if j < len_dt - 1:
            # if i < len_datasets_run - 1:
            logs[-1]['already_done'] += 1
            clear_cmd()
            # break
        dataframe = pd.DataFrame(data_dict)
        dataset_name = 'inter_' + datetime_to_plain_text(data_hora_ant) + '_' + \
                              datetime_to_plain_text(data_hora_dep) + '.csv'
        dataframe.to_csv(util.PATH_INTER_DATASETS + dataset_name, index=False)
        # break
    header()
    status(logs)
    print('-' * 119)


if __name__ == '__main__':
    # clean_datasets()
    generate_reports()

import os
import pandas as pd
from datetime import datetime
from matplotlib import pyplot


PATH_RAW_DATASETS = 'C:\\Users\\Rafae\\OneDrive\\Documentos\\projeto_iniciacao_cientifica\\ifgoiano_site\\datasets\\raw'
PATH_INTER_DATASETS = 'C:\\Users\\Rafae\\OneDrive\\Documentos\\projeto_iniciacao_cientifica\\ifgoiano_site\\datasets\\inter'
CHART_PATH = 'C:\\Users\\Rafae\\OneDrive\\Documentos\\projeto_iniciacao_cientifica\\ifgoiano_site\\chart'


def read_latest_dataset():
    with os.scandir(PATH_RAW_DATASETS) as dir_entries:
        filename = dir_entries.__next__().name
        for dir_entry in dir_entries:
            dt_from_filename = get_execution_datetime(filename)
            dt_from_dir_entry = get_execution_datetime(dir_entry.name)
            if dt_from_dir_entry > dt_from_filename:
                filename = dir_entry.name
    return read_dataset(filename)


def read_dataset(dataset_name):
    df = pd.read_csv(f'{PATH_RAW_DATASETS}{dataset_name}')
    df = clean_dataset(df)
    df['data_hora'] = pd.to_datetime(df['data_hora'])
    return df


def clean_dataset(dt):
    dt = dt[dt['acessos'].notna()].reset_index()
    dt = dt.drop_duplicates(subset=['titulo', 'data_hora']).reset_index()
    cols = dt.columns
    valid_cols = ['titulo', 'descricao', 'data_hora', 'dia_semana',
                  'periodo_dia', 'imagens', 'acessos', 'acessos_medio_hora',
                  'tem_imagem_perfil']
    cols_to_drop = list()
    for col in cols:
        if col not in valid_cols:
            cols_to_drop.append(col)
    if len(cols_to_drop) > 0:
        dt = dt.drop(cols_to_drop, axis=1)
    return dt


def get_execution_datetime(dataset_name):
    split_dataset_name = str(dataset_name).split('_')
    year = int(split_dataset_name[2])
    month = int(split_dataset_name[3])
    day = int(split_dataset_name[4])
    hour = int(split_dataset_name[5])
    minute = int(split_dataset_name[6])
    sec = int(split_dataset_name[7])
    return datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=sec)


def get_datasets():
    with os.scandir(PATH_RAW_DATASETS) as dir_entries:
        dataset_names = list()
        for entry in dir_entries:
            dataset_names.append(entry.name)
        return sorted(dataset_names, key=get_execution_datetime)


def chart(kind, dataset, x_label, y_label, x_col, y_col, title, path, rotation=None):
    pyplot.xlabel(x_label)
    pyplot.ylabel(y_label)
    pyplot.title(title)
    pyplot.ticklabel_format(style='plain')
    if rotation:
        pyplot.xticks(rotation=int(rotation))
    kind_lower = kind.lower()
    if kind_lower == 'bar':
        pyplot.bar(dataset[x_col], dataset[y_col])
    elif kind_lower == 'plot':
        pyplot.plot(dataset[x_col], dataset[y_col])
    else:
        raise ValueError(f'Unknown chart kind')
    if not os.path.exists(path):
        os.makedirs(path)
    pyplot.savefig(os.path.join(path, title.lower().replace(' ', '_').replace('/', '_') + '.png'), bbox_inches='tight')
    pyplot.show()


def error_chart(dataset, x_label, y_label, x_col, y_col, y_err_col, title, path, axhline_value, axhline_label,
                rotation=None):
    pyplot.xlabel(x_label)
    pyplot.ylabel(y_label)
    pyplot.title(title)
    pyplot.axhline(y=axhline_value, color='r', linestyle='dashed', label=axhline_label)
    pyplot.legend(bbox_to_anchor=(.85, 1), loc='upper center')
    if rotation:
        pyplot.xticks(rotation=int(rotation))
    pyplot.errorbar(
        x=dataset[x_col],
        y=dataset[y_col],
        yerr=dataset[y_err_col],
        marker='^'
    )
    if not os.path.exists(path):
        os.makedirs(path)
    pyplot.savefig(os.path.join(path, title.lower().replace(' ', '_').replace('/', '_') + '.png'), bbox_inches='tight')
    pyplot.show()


def day_period_to_num(day_period):
    if day_period == 'manha':
        return 0
    elif day_period == 'tarde':
        return 1
    elif day_period == 'noite':
        return 2
    else:
        raise ValueError(f'Unknown day period: {day_period}')


def weekday_to_num(weekday):
    if weekday == 'domingo':
        return 0
    elif weekday == 'segunda':
        return 1
    elif weekday == 'terca':
        return 2
    elif weekday == 'quarta':
        return 3
    elif weekday == 'quinta':
        return 4
    elif weekday == 'sexta':
        return 5
    elif weekday == 'sabado':
        return 6
    else:
        raise ValueError(f'Unknown weekday: {weekday}')


def weekday_day_period_to_num(weekday_day_period):
    split_data = weekday_day_period.split('/')
    weekday_num, day_period_num = weekday_to_num(split_data[0]), day_period_to_num(split_data[1])
    return 3 * weekday_num + day_period_num

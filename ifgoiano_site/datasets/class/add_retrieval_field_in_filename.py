import pandas as pd
import os
import datetime


if __name__ == '__main__':
    files = [file for file in os.listdir(os.getcwd()) if file.endswith('.csv')]
    for file in files:
        df = pd.read_csv(file)
        new_file = file.replace('pubs_data_', '').replace('.csv', '')
        split = new_file.split('_')
        new_split = split[:-3:]
        date_part = '-'.join(new_split[:3])
        time_part = ':'.join(new_split[-3::])
        df['data_coleta'] = ' '.join([date_part, time_part])
        df.to_csv(file, index=False)
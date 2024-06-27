import os, pandas, scipy, numpy


SOURCE_PATH = 'C:\\Users\\Rafae\\OneDrive\\Documentos\\projeto_iniciacao_cientifica\\ifgoiano_site\\datasets\\raw'
TARGET_PATH = 'C:\\Users\\Rafae\\OneDrive\\Documentos\\projeto_iniciacao_cientifica\\ifgoiano_site\\datasets\\clean'


def clear_exceeding_commas(file='C:\\Users\\Rafae\\OneDrive\\Documentos\\projeto_iniciacao_cientifica\\ifgoiano_site\\datasets\\raw\\pubs_data_2023_01_26_21_00_04_4_20_19.csv'):
    with open(
        file,
        'r',
        encoding='utf-8'
    ) as f_read:
        lines = f_read.readlines()
        new_content = ''
        for line in lines:
            i = len(line) - 2
            while line[i] == ',':
                i -= 1
            new_content += line[:i + 1] + '\n'
        with open(
            file,
            'w',
            encoding='utf-8'
        ) as f_write:
            f_write.write(new_content)
        print('Done')


def clear_csv(file):
    csv = pandas.read_csv(file)
    csv = csv.dropna()
    return csv[(numpy.abs(scipy.stats.zscore(csv['acessos'])) < 3)]  # Get outliers out.


if __name__ == '__main__':
    files = os.listdir(SOURCE_PATH)
    i = 0
    for f in files:
        clean_csv = clear_csv(os.path.join(SOURCE_PATH, f))
        clean_csv.to_csv(os.path.join(TARGET_PATH, f), index=False)
        i += 1

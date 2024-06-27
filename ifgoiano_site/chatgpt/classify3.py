import os, pandas
from classify2 import SOURCE_PATH, TARGET_PATH
from process import EXPORT_ARGS


if __name__ == '__main__':
    files = os.listdir(SOURCE_PATH)
    df1 = pandas.read_csv(os.path.join(TARGET_PATH, files[-1]))
    for f in files[:len(files) - 1]:
        df2 = pandas.read_csv(os.path.join(SOURCE_PATH, f))
        diff = df1.shape[0] - df2.shape[0]
        df2['assunto'] = '-'
        for i in range(df2.shape[0] - 1, -1, -1):
            title2, desc2 = df2.loc[i, ['titulo', 'descricao']]
            title1, desc1 = df1.loc[i + diff, ['titulo', 'descricao']]
            if title2 != title1 and desc2 != desc1:
                assunto = '-'
            else:
                assunto = df1.loc[i + diff, 'assunto']
            df2.loc[i, 'assunto'] = assunto
        df2.to_csv(os.path.join(TARGET_PATH, f), **EXPORT_ARGS)
import os, pandas
from classify2 import SOURCE_PATH, TARGET_PATH
from process import EXPORT_ARGS


if __name__ == '__main__':
    files = os.listdir(TARGET_PATH)
    for f in files:
        df = pandas.read_csv(os.path.join(TARGET_PATH, f))
        df = df.drop(df[df['assunto'] == '-'].index)
        df.to_csv(os.path.join(TARGET_PATH, f), **EXPORT_ARGS)
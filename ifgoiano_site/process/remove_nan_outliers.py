import os, pandas, scipy, numpy

SOURCE_PATH = ''
TARGET_PATH = ''

if __name__ == '__main__':
    files = os.listdir(SOURCE_PATH)
    for f in files:
        csv = pandas.read_csv(os.path.join(SOURCE_PATH, f))
        csv.dropna(inplace=True)
        csv_zscore = scipy.stats.zscore(csv['acessos'])
        csv_zscore_abs = (numpy.abs(csv_zscore) < 3)
        csv = csv[csv_zscore_abs]
        csv.to_csv(os.path.join(TARGET_PATH, f), index=False)




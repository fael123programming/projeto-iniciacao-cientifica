import os, pandas
from classify2 import SOURCE_PATH, TARGET_PATH



if __name__ == '__main__':
    # df = pandas.read_csv(os.path.join(TARGET_PATH, 'pubs_data_2023_02_02_23_18_22_4_23_26.csv'))
    # df2 = pandas.read_csv(os.path.join(TARGET_PATH, 'pubs_data_2023_02_03_21_00_04_4_20_12.csv'))
    files = os.listdir(TARGET_PATH)
    # d = list()
    c = 0
    df1 = pandas.read_csv(os.path.join(TARGET_PATH, files[0]))
    for i in range(1, len(files)):
        df2 = pandas.read_csv(os.path.join(TARGET_PATH, files[i]))
        diff = df2.shape[0] - df1.shape[0]
        for j in range(df1.shape[0] - 1, diff - 1, -1):
            # t1, d1 = df1.loc[j, ['titulo', 'descricao']]             
            # t2, d2 = df2.loc[j - diff, ['titulo', 'descricao']]
            dt1 = df1.loc[j, 'data_hora']
            dt2 = df2.loc[j-diff, 'data_hora']
            if dt1 != dt2:
                print(dt1, dt2)
                c += 1
        # exit(0)
        # for j in range(i + 1, len(files)):
        #     df2 = pandas.read_csv(os.path.join(TARGET_PATH, files[j]))
            
        #     diff = df2.shape[0] - df1.shape[0]
        #     for p in range(df2.shape[0] - 1, diff - 1, -1):
        #         try:
        #         except:
        #             print(f'{p - diff} {p}')
        #             print(f'{df1.shape[0]} {df2.shape[0]}')
        #             d.append([[t1, t2], [d1, d2]])
    print('Found:', c)
    # for e in d:
        # print(e)


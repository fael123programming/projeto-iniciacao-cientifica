import pandas as pd
import numpy as np
from scipy import stats


df = pd.DataFrame(
    [
        {'name': 'Paul', 'age': 18}, 
        {'name': 'Marcus', 'age': 23}, 
        {'name': 'Ana', 'age': 28},
        {'name': 'Rafael', 'age': 50}, 
        {'name': 'Pedro', 'age': 8}, 
        {'name': 'Mariana', 'age': 37},
        {'name': 'Jorge', 'age': 66}, 
        {'name': 'Isabel', 'age': 56}, 
        {'name': 'Jurge', 'age': 10},
        {'name': 'Lara', 'age': 22}, 
        {'name': 'Henderson', 'age': 30}, 
        {'name': 'Julio', 'age': 70},
        {'name': 'Mathusalen', 'age': 979}
    ]
)
zed = stats.zscore(df['age'])
print(zed)
# abso = (np.abs(zed) < 3)
# df = df[abso]
# print(df)

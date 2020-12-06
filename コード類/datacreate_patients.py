import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import random

result_full_df = pd.read_csv('result_full.csv', index_col=0, encoding='shift_jis')

result_full_df.drop(columns='index', inplace=True)
result_full_df.drop(columns='p_name', inplace=True)
result_full_df.drop(columns='sex', inplace=True)
result_full_df.drop(columns='h_name', inplace=True)
result_full_df.drop(columns='possible', inplace=True)
result_full_df.drop(columns='patient_text', inplace=True)
result_full_df.drop(columns='doctor_text', inplace=True)
result_full_df.rename(columns={'expert': 'department'}, inplace=True)
result_full_df.reindex(columns=['patient_id', 'department', 'desired', 'doctor_id'])

# print(result_full_df)

# status
status_df = DataFrame(np.array([0, 0, 1, 1, 2, 2]).reshape(3, 2), columns=['status', 'status2'])
print(status_df)
# 仮のデータフレーム作成
x = pd.concat([result_full_df.iloc[0], status_df.iloc[0]])
print(x)
y = pd.concat([result_full_df.iloc[1], status_df.iloc[1]])
patients_df = pd.DataFrame([x, y])
print(patients_df)

# データフレーム作成
# len(result_full_df.index)
k = len(patients_df.index)
for i in range(len(result_full_df.index)):
    user = result_full_df.iloc[i]
    for j in range(len(status_df.index)):
        doctor = status_df.iloc[j]
        result = pd.concat([user, doctor])
        patients_df.loc[k] = result
        k += 1
        # print(str(j) + ' / ' + str(len(doctor_df.index)))
    print(str(i) + ' / ' + str(len(result_full_df.index)))
print(patients_df)
patients_df.drop(columns='status2', inplace=True)
patients_df.drop(patients_df.index[[0, 1]], inplace=True)
patients_df = patients_df.reset_index()
# データの保存
patients_df.to_csv('patients.csv', index=True, encoding='shift_jis')

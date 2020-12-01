from faker import Faker
import pandas as pd
from pandas import Series, DataFrame
import random
import numpy as np

# データの要素の作成
#################################################################################################################
fake = Faker('ja_JP')

# データの個数
n = 300

# id
id_list = list(range(n))

# 医者の名前, 病院の名前
hospital_variations = ['医院', 'クリニック', '病院']
name_list = []
hospital_name_list = []
for i in range(n):
    name = fake.name()
    hospital_name = name.split()[0] + hospital_variations[i % len(hospital_variations)]
    name_list.append(name)
    hospital_name_list.append(hospital_name)

# 座標 (0 - 10000)
address_x = [random.randint(0, 10000) for _ in range(n)]
address_y = [random.randint(0, 10000) for _ in range(n)]

# 専門
expert_variations = ['内科', '外科', '耳鼻科', '眼科', '内科', '内科', '外科']
expert_list = []
expert_num_list = []
for i in range(n):
    expert = expert_variations[i % len(expert_variations)]
    if expert == '内科':
        expert_num = 0
    elif expert == '外科':
        expert_num = 1
    elif expert == '耳鼻科':
        expert_num = 2
    else:
        expert_num = 3
    expert_list.append(expert)
    expert_num_list.append(expert_num)

# 混雑度　(0 - 1)
congestion_list = [random.random() for _ in range(n)]
# print(congestion_list)

# オンライン対応
possible_variation = [0, 1, 1, 0, 1, 1, 1]
possible_list = [possible_variation[i % len(possible_variation)] for i in range(n)]
# print(possible_list)

# url
url_list = [fake.url() for _ in range(n)]

#################################################################################################################

# データフレームの作成
#################################################################################################################
hospital_df = DataFrame({'id': id_list,
                         'name': name_list,
                         'hospital_name': hospital_name_list,
                         'address_x': address_x,
                         'address_y': address_y,
                         'expert': expert_list,
                         'congestion': congestion_list,
                         'possible': possible_list,
                         'url': url_list})

hospital_df.set_index('id', inplace=True)
# print(hospital_df)

# データフレームの保存
# hospital_df.to_csv('hospitaldata.csv', index=True)

#################################################################################################################






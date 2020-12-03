from faker import Faker
import pandas as pd
from pandas import Series, DataFrame
import random
import numpy as np
import requests
import json
import time

json_url = 'http://geoapi.heartrails.com/api/json?method=searchByGeoLocation'
wait_time = 1


def get_data(lug,lat):
    payload = {'method': 'searchByGeoLocation', 'x': lug, 'y': lat}
    try:
        ret = requests.get(json_url, params=payload)
        json_ret = ret.json()
    except requests.exceptions.RequestException as e:
        print("ErrorContent: ",e)

    return json_ret


# 住所データの整形関数
def serealize_data(data):
    try:
        dic = data['response']['location'][0]
        det = str(dic['prefecture'] + dic['city'] + dic['town'])
        return det
    except KeyError as e:
        print(e)


# 軽度・緯度に使う乱数の生成
def gene_number(lug_fnum, lug_lnum, lat_fnum, lat_lnum):
    lug = round(random.uniform(lug_fnum,lug_lnum),5)
    lat = round(random.uniform(lat_fnum,lat_lnum),5)
    return lug,lat


# データの要素の作成
#################################################################################################################
fake = Faker('ja_JP')

# データの個数
n = 10

# id
id_list = list(range(n))

# 氏名, 性別
name_list = []
sex_list = []
sex_var = ['男性', '女性']
for i in range(n):
    sex = random.choice(sex_var)
    if sex == '男性':
        name = fake.name_male()
        name_list.append(name)
        sex_list.append(sex)
    else:
        name = fake.name_female()
        name_list.append(name)
        sex_list.append(sex)

# 専門選択
expert_variations = ['内科', '外科', '耳鼻科', '眼科']
expert_list = [random.choice(expert_variations) for _ in range(n)]

# 希望　オンライン or 来院
possible_variation = ['オンライン', '来院']
possible_list = [random.choice(possible_variation) for _ in range(n)]

# 来院の場合の優先条件（距離 or 混雑度）
priority_var = ['距離', '混雑度']
priority_list = [random.choice(priority_var) if possible_list[i] == '来院' else None for i in range(n)]

# 現在地（住所、経緯度）
street_address_list = []
address_x = []
address_y = []
i = 1
while True:
    if i > n:
        break
    lug, lat = gene_number(138.0, 140.0, 35.0, 37.0)
    ret = get_data(lug, lat)
    data = serealize_data(ret)
    print(data)
    if data != None:
        street_address_list.append(data)
        address_x.append(lug)
        address_y.append(lat)
        print(str(i) + ' / ' + str(n))
        i += 1
    time.sleep(wait_time)

#################################################################################################################

# データフレームの作成
#################################################################################################################
hospital_df = DataFrame({'id': id_list,
                         'name': name_list,
                         'sex': sex_list,
                         'choice_expert': expert_list,
                         'online_or_visit': possible_list,
                         'choice_priority': priority_list,
                         'street_address_now': street_address_list,
                         'address_x': address_x,
                         'address_y': address_y,
                         })

hospital_df.set_index('id', inplace=True)
# print(hospital_df)

# データフレームの保存
# hospital_df.to_csv('hospitaldata.csv', index=True)
hospital_df.to_csv('userdata.csv', index=True, encoding='shift_jis')
#################################################################################################################

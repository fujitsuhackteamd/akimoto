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
        postal = str(dic['postal'])
        postal = postal[:3] + '-' + postal[3:]
        det = str(dic['prefecture'] + dic['city'] + dic['town'])
        return postal, det
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
n = 700

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
# address_x = [random.randint(0, 10000) for _ in range(n)]
# address_y = [random.randint(0, 10000) for _ in range(n)]

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

# 郵便番号、住所、経緯度
postal_list = []
street_address_list = []
address_x = []
address_y = []
i = 1
while True:
    if i > n:
        break
    lug, lat = gene_number(129.0, 140.0, 33.0, 39.0)
    ret = get_data(lug, lat)
    data = serealize_data(ret)
    if data != None:
        postal = data[0]
        street_address = data[1]
        postal_list.append(postal)
        street_address_list.append(street_address)
        address_x.append(lug)
        address_y.append(lat)
        print(str(i) + ' / ' + str(n))
        i += 1
    time.sleep(wait_time)

# 電話番号
phonenumber_list = [fake.phone_number() for _ in range(n)]


#################################################################################################################

# データフレームの作成
#################################################################################################################
hospital_df = DataFrame({'id': id_list,
                         'name': name_list,
                         'hospital_name': hospital_name_list,
                         'expert': expert_list,
                         'postal': postal_list,
                         'street_address': street_address_list,
                         'phone_number': phonenumber_list,
                         'address_x': address_x,
                         'address_y': address_y,
                         'congestion': congestion_list,
                         'possible': possible_list,
                         'url': url_list})

hospital_df.set_index('id', inplace=True)
# print(hospital_df)

# データフレームの保存
# hospital_df.to_csv('hospitaldata.csv', index=True)
hospital_df.to_csv('hospitaldata_v2.csv', index=True, encoding='shift_jis')
#################################################################################################################






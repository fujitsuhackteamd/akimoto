import pandas as pd
from pandas import Series, DataFrame
import random

hospital_df = pd.read_csv('hospitaldata_v2.csv', index_col=0, encoding='shift_jis')
user_df = pd.read_csv('userdata_v2.csv', index_col=0, encoding='shift_jis')
# print(user_df)
# print(type(user_df))

# 症状(オンライン、来院)
#############################################################################################################
# 内科
sym_internal_onl = ['身体のだるさ', '鼻水', 'のどの痛み', '咳']
sym_internal_vis = ['発熱', '腹痛', '神経痛']


# 外科
sym_surgery_onl = ['動かすと痛み', '肌の痛み', 'にきび']
sym_surgery_vis = ['動かすとかなりの痛み', '出血']

# 耳鼻科
sym_otorhin_onl = ['くしゃみ', '鼻水', '目のかゆみ', '花粉症']
sym_otorhin_vis = ['頭痛', '耳の痛み', '聞こえが悪い', '発熱']


# 眼科
sym_ophthal_onl = ['目のかゆみ', 'めやに', 'アレルギー']
sym_ophthal_vis = ['目の痛み', '目のかすみ', '充血']


#############################################################################################################


# # 診察結果
# #############################################################################################################
# # 内科
# res_internal_onl = ['風邪', '疲労']
# res_internal_vis = ['インフルエンザ', 'コロナの疑い', '熱']
#
# # 外科
# res_surgery_onl = ['突き指', '日焼け', 'にきび']
# res_surgery_vis = ['骨折', '捻挫', '擦り傷', '刺し傷']
#
# # 耳鼻科
# res_otorhin_onl = ['花粉症', '風邪', 'アレルギー']
# res_otorhin_vis = ['中耳炎', 'コロナの疑い', '熱']
#
#
# # 眼科
# res_ophthal_onl = ['花粉症', 'ドライアイ', 'アレルギー']
# res_ophthal_vis = ['結膜炎', 'ものもらい']
#
#
# #############################################################################################################


# データ結合
#############################################################################################################
# 患者と症状の紐づけ
patients_text_list = []

for i in range(len(user_df.index)):
    user = user_df.iloc[i]
    user_expert = user['choice_expert']
    user_choice = user['online_or_visit']
    # print(type(user))
    # print(user_expert)
    if user_expert == '内科':
        if user_choice == 'オンライン':
            user_text = random.sample(sym_internal_onl, random.randint(1, len(sym_internal_onl) - 1))
            user_text = '、'.join(user_text)
            print(user_text)
            patients_text_list.append(user_text)
        else:
            user_text = random.sample(sym_internal_vis, random.randint(1, len(sym_internal_vis)))
            user_text = '、'.join(user_text)
            print(user_text)
            patients_text_list.append(user_text)
    elif user_expert == '外科':
        if user_choice == 'オンライン':
            user_text = random.sample(sym_surgery_onl, 1)
            user_text = '、'.join(user_text)
            print(user_text)
            patients_text_list.append(user_text)
        else:
            user_text = random.sample(sym_surgery_vis, 1)
            user_text = '、'.join(user_text)
            print(user_text)
            patients_text_list.append(user_text)
    elif user_expert == '耳鼻科':
        if user_choice == 'オンライン':
            user_text = random.sample(sym_otorhin_onl, random.randint(1, len(sym_otorhin_onl) - 1))
            user_text = '、'.join(user_text)
            print(user_text)
            patients_text_list.append(user_text)
        else:
            user_text = random.sample(sym_otorhin_vis, random.randint(1, len(sym_otorhin_vis) - 1))
            user_text = '、'.join(user_text)
            print(user_text)
            patients_text_list.append(user_text)
    else:
        if user_choice == 'オンライン':
            user_text = random.sample(sym_ophthal_onl, random.randint(1, len(sym_ophthal_onl)))
            user_text = '、'.join(user_text)
            print(user_text)
            patients_text_list.append(user_text)
        else:
            user_text = random.sample(sym_ophthal_vis, random.randint(1, len(sym_ophthal_vis)))
            user_text = '、'.join(user_text)
            print(user_text)
            patients_text_list.append(user_text)
# print(patients_text_list)

# 患者データの整理
user_df_copy = user_df.copy()
user_df_copy.drop(columns='street_address_now', inplace=True)
user_df_copy.drop(columns='address_x', inplace=True)
user_df_copy.drop(columns='address_y', inplace=True)
user_df_copy.drop(columns='choice_priority', inplace=True)
user_df_copy.rename(columns={'online_or_visit': 'desired'}, inplace=True)
user_df_copy.loc[user_df_copy['desired'] == 'オンライン', 'desired'] = 0
user_df_copy.loc[user_df_copy['desired'] == '来院', 'desired'] = 1
user_df_copy['patient_text'] = patients_text_list
user_df_copy.rename(columns={'name': 'p_name'}, inplace=True)
user_df_copy['patient_id'] = list(range(len(user_df_copy.index)))
# user_df_copy.rename(columns={'id': 'patient_id'}, inplace=True)
# print(user_df_copy)

# 病院データの整理
hospital_df.drop(columns='street_address', inplace=True)
hospital_df.drop(columns='address_x', inplace=True)
hospital_df.drop(columns='address_y', inplace=True)
hospital_df.drop(columns='congestion', inplace=True)
hospital_df.drop(columns='url', inplace=True)
hospital_df.drop(columns='phone_number', inplace=True)
hospital_df.drop(columns='postal', inplace=True)
hospital_df.drop(columns='hospital_name', inplace=True)
# hospital_df.rename(columns={'id': 'doctor_id'}, inplace=True)
hospital_df.rename(columns={'name': 'h_name'}, inplace=True)
hospital_df['doctor_id'] = list(range(len(hospital_df.index)))
print(hospital_df)

# 病院と診療結果の紐づけ
# doctor_text_list = []
#
# for i in range(len(hospital_df.index)):
#     hospital = hospital_df.iloc[i]
#     hospital_expert = hospital['expert']
#     hospital_possible = hospital['possible']
#     if hospital_expert == '内科':
#         if hospital_possible == 0:
#             doctor_text = random.choice(res_internal_onl)
#             print(doctor_text)
#             doctor_text_list.append(doctor_text)
#         else:
#             doctor_text = random.choice(res_internal_vis)
#             print(doctor_text)
#             doctor_text_list.append(doctor_text)
#     elif hospital_expert == '外科':
#         if hospital_possible == 0:
#             doctor_text = random.choice(res_surgery_onl)
#             print(doctor_text)
#             doctor_text_list.append(doctor_text)
#         else:
#             doctor_text = random.choice(res_surgery_vis)
#             print(doctor_text)
#             doctor_text_list.append(doctor_text)
#     elif hospital_expert == '耳鼻科':
#         if hospital_possible == 0:
#             doctor_text = random.choice(res_otorhin_onl)
#             print(doctor_text)
#             doctor_text_list.append(doctor_text)
#         else:
#             doctor_text = random.choice(res_otorhin_vis)
#             print(doctor_text)
#             doctor_text_list.append(doctor_text)
#     else:
#         if hospital_possible == 0:
#             doctor_text = random.choice(res_ophthal_onl)
#             print(doctor_text)
#             doctor_text_list.append(doctor_text)
#         else:
#             doctor_text = random.choice(res_ophthal_vis)
#             print(doctor_text)
#             doctor_text_list.append(doctor_text)

# データフレームの保存
# user_df_copy.to_csv('user_sym.csv', index=True, encoding='shift_jis')
# hospital_df.to_csv('doctor.csv', index=True, encoding='shift_jis')
#############################################################################################################

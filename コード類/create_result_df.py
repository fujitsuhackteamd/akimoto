import pandas as pd
from pandas import Series, DataFrame
import random

# データ結合
# doctor_df = pd.read_csv('doctor.csv', index_col=0, encoding='shift_jis')
# user_sym_df = pd.read_csv('user_sym.csv', index_col=0, encoding='shift_jis')
#
# # 仮のデータフレーム作成
# x = pd.concat([user_sym_df.iloc[0], doctor_df.iloc[0]])
# y = pd.concat([user_sym_df.iloc[1], doctor_df.iloc[1]])
# result_df = pd.DataFrame([x, y])
# print(result_df)
#
# # データフレーム作成
# k = len(result_df.index)
# for i in range(len(user_sym_df.index)):
#     user = user_sym_df.iloc[i]
#     for j in range(len(doctor_df.index)):
#         doctor = doctor_df.iloc[j]
#         result = pd.concat([user, doctor])
#         result_df.loc[k] = result
#         k += 1
#         # print(str(j) + ' / ' + str(len(doctor_df.index)))
#     print(str(i) + ' / ' + str(len(user_sym_df.index)))
# print(result_df)

# 保存
# result_df.to_csv('result.csv', index=True, encoding='shift_jis')

# 余分なデータの削除
#############################################################################################################
result_df = pd.read_csv('result（仮）.csv', index_col=0, encoding='shift_jis')

drop_index_1 = result_df.index[result_df['choice_expert'] != result_df['expert']]
result_df = result_df.drop(drop_index_1)
# print(result_df)
drop_index_2 = result_df.index[result_df['possible'] != result_df['desired']]
result_df = result_df.drop(drop_index_2)
# print(result_df)
result_df = result_df.reset_index()
# print(result_df)

#############################################################################################################

# 診療結果の追加
#############################################################################################################
# 診察結果
# 内科
res_internal_onl = ['風邪', '疲労']
res_internal_vis = ['インフルエンザ', 'コロナの疑い', '熱']

# 外科
res_surgery_onl = ['突き指', '日焼け', 'にきび']
res_surgery_vis = ['骨折', '捻挫', '擦り傷', '刺し傷']

# 耳鼻科
res_otorhin_onl = ['花粉症', '風邪', 'アレルギー']
res_otorhin_vis = ['中耳炎', 'コロナの疑い', '熱']


# 眼科
res_ophthal_onl = ['花粉症', 'ドライアイ', 'アレルギー']
res_ophthal_vis = ['結膜炎', 'ものもらい']

# 診療結果の紐づけ
doctor_text_list = []

for i in range(len(result_df.index)):
    hospital = result_df.iloc[i]
    hospital_expert = hospital['expert']
    hospital_possible = hospital['possible']
    patient_text = hospital['patient_text']
    if hospital_expert == '内科':
        if hospital_possible == 0:
            doctor_text = random.choice(res_internal_onl)
            print(doctor_text)
            doctor_text_list.append(doctor_text)
        else:
            doctor_text = random.choice(res_internal_vis)
            print(doctor_text)
            doctor_text_list.append(doctor_text)
    elif hospital_expert == '外科':
        if hospital_possible == 0:
            if patient_text == '動かすと痛み':
                doctor_text = res_surgery_onl[0]
            elif patient_text == '肌の痛み':
                doctor_text = res_surgery_onl[1]
            else:
                doctor_text = res_surgery_onl[2]
            print(doctor_text)
            doctor_text_list.append(doctor_text)
        else:
            if patient_text == '動かすとかなりの痛み':
                doctor_text = random.choice(res_surgery_vis[:2])
            else:
                doctor_text = random.choice(res_surgery_vis[2:])
            print(doctor_text)
            doctor_text_list.append(doctor_text)
    elif hospital_expert == '耳鼻科':
        if hospital_possible == 0:
            if '花粉症' in patient_text:
                doctor_text = res_otorhin_onl[0]
            else:
                doctor_text = random.choice(res_otorhin_onl[1:])
            print(doctor_text)
            doctor_text_list.append(doctor_text)
        else:
            doctor_text = random.choice(res_otorhin_vis)
            print(doctor_text)
            doctor_text_list.append(doctor_text)
    else:
        if hospital_possible == 0:
            doctor_text = random.choice(res_ophthal_onl)
            print(doctor_text)
            doctor_text_list.append(doctor_text)
        else:
            doctor_text = random.choice(res_ophthal_vis)
            print(doctor_text)
            doctor_text_list.append(doctor_text)
result_df['doctor_text'] = doctor_text_list

# データの保存
# result_df.to_csv('result_full.csv', index=True, encoding='shift_jis')

# データの整理
result_df.drop(columns='index', inplace=True)
result_df.drop(columns='p_name', inplace=True)
result_df.drop(columns='sex', inplace=True)
result_df.drop(columns='choice_expert', inplace=True)
result_df.drop(columns='h_name', inplace=True)
result_df.drop(columns='possible', inplace=True)
result_df.reindex(columns=['patient_id', 'patient_text', 'doctor_id', 'doctor_text', 'desired'])

# データの保存
# result_df.to_csv('result.csv', index=True, encoding='shift_jis')







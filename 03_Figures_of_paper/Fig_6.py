import os
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager

# the file of experts score
expert_score_json_path = r'G:\202106FMS_data\Dataset_of_FMS\experts_score.json'
# the path of saving the file of Fig_6.
pic_save_path = r'E:\Fig_6.pdf'

# 01. start-Data preparation
# get the expert score distribution of the movements of FMS

with open(expert_score_json_path, encoding='utf-8') as f:
    json_data_dic = json.load(f)

# the list is used to saved the expert score distribution of the movements by per subject
all_subjects_list = [[] for i in range(45)]

count_s = 0     # the count of subjects
for (key_root, value_root) in json_data_dic.items():
    count_s += 1
    # print(key_root)
    count_m = 0     # the count of movements
    for (key_s, value_s) in value_root.items():
        count_m += 1
        # print(key_s)
        count_e = 0 # # the count of episodes
        m_sum = 0   # the sum of all episodes of one movement.
        for (key_m, value_m) in value_s.items():
            # print(value_m)
            count_e += 1
            # print(sum(value_m))
            m_sum = m_sum + sum(value_m)
        # print(m_sum/(count_e*3))
        per_movement_average_score = round(m_sum / (count_e * 3))
        all_subjects_list[count_s-1].append(per_movement_average_score)

# the list is used to saved the expert score distribution of the (15) movements
all_movements_list = [[0, 0, 0] for i in range(15)]

for i in range(15):
    for j in range(len(all_subjects_list)):
        if all_subjects_list[j][i] == 1:
            all_movements_list[i][0] += 1
        if all_subjects_list[j][i] == 2:
            all_movements_list[i][1] += 1
        if all_subjects_list[j][i] == 3:
            all_movements_list[i][2] += 1

# 01. end-Data preparation

# 02. plot——start

# Set global font and fontsize
font_manager.fontManager.addfont(r'C:\Users\Xingqingjun\AppData\Local\Microsoft\Windows\Fonts\Helvetica.ttf')
plt.rcParams['font.sans-serif'] = 'Helvetica'
plt.rcParams['font.size'] = '16'

# the labels of x-axis.
results = {}
for index, each_m in enumerate(all_movements_list):
    key_str = "m" + str(index + 1).zfill(2)
    results[key_str] = each_m
labels = results.keys()

score_arr = np.array(all_movements_list)
score_one_arr = score_arr[:, 0]
score_two_arr = score_arr[:, 1]
score_three_arr = score_arr[:, 2]

score_one_list = score_one_arr.tolist()
score_two_list = score_two_arr.tolist()
score_three_list = score_three_arr.tolist()

x = np.arange(len(labels))  # the label locations
width = 0.3  # the width of the bars

fig, ax = plt.subplots(figsize=(15.2, 8.1))
rects1 = ax.bar(x - width, score_one_list, width, label='1 score')
rects2 = ax.bar(x, score_two_list, width, label='2 score')
rects3 = ax.bar(x + width, score_three_list, width, label='3 score')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Frequency (n)', labelpad=8)
ax.set_xlabel('Movements of FMS', labelpad=8)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

# Remove the top and bottom borders
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

fig.tight_layout()

# plt.show()
plt.savefig(pic_save_path, bbox_inches='tight', dpi=300)

# 02. plot——end
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

# 01. start-Data preparation

# To save the CSV files that recorded the frequency of no-body frames in 'Front' and 'Side' sensors.
# Front.csv and Side.csv are saved in our dataset.
nobody_csv_file_list = [r'G:\Dataset of FMS\Preprocessing files\Statistics of frames without skeleton\Front.csv',
                        r'G:\Dataset of FMS\Preprocessing files\Statistics of frames without skeleton\Side.csv']

# the path of saving the file of Fig_4_1.
pic_save_path = r'E:\Fig_4_1.pdf'

movement_title_list = [[], []]  # the list is saved the movement_num of "Front" and "Side".
no_bodies_frames_rate_list = [[], []]   # the list is saved the no_bodies_frames_rate of "Front" and "Side".

for i in range(len(nobody_csv_file_list)):
    df = pd.read_csv(nobody_csv_file_list[i])
    df_rows = df.shape[0]
    for j in range(df_rows):
        if df["no_bodies_frames_rate"][j] >= 0.01:
            # the position of movement_num in json_name is different for "Front" and "Side"
            if i == 0:
                movement_num = df["json_name"][j][10:13]
            elif i == 1:
                movement_num = df["json_name"][j][9:12]
            # print(movement_num)
            movement_title_list[i].append(movement_num)
            no_bodies_frames_rate_list[i].append(df["no_bodies_frames_rate"][j])
# print(len(no_bodies_frames_rate_list))

# the list is used to save the distribution of no-body frames.
# all_movements_list[i][0] ———— ( 0.4, 1.0]
# all_movements_list[i][1] ———— ( 0.1, 0.4]
# all_movements_list[i][2] ———— (0.01, 0.1]
all_movements_list = [[[i * 0 for i in range(15)] for j in range(3)] for k in range(2)]

# all_movements_list[i][0] ———— ( 0.4, 1.0]
for i in range(2):
    for index, value in enumerate(no_bodies_frames_rate_list[i]):
        index_ = int(movement_title_list[i][index][1:]) - 1
        if value >= 0.4:
            all_movements_list[i][0][index_] += 1   # all_movements_list[i][0] ———— ( 0.4, 1.0]
        if 0.4 > value >= 0.1:
            all_movements_list[i][1][index_] += 1   # all_movements_list[i][1] ———— ( 0.1, 0.4]
        if 0.1 > value >= 0.01:
            all_movements_list[i][2][index_] += 1   # all_movements_list[i][2] ———— (0.01, 0.1]
# print(all_movements_list)

# the labels of x-axis
labels = ['m' + str(i).zfill(2) for i in range(1, 16)]

# the distribution of no-body frames in "Front"
front_level_1_list = all_movements_list[0][0]
front_level_2_list = all_movements_list[0][1]
front_level_3_list = all_movements_list[0][2]

# the distribution of no-body frames in "Side"
side_level_1_list = pd.Series(all_movements_list[1][0])
side_level_2_list = pd.Series(all_movements_list[1][1])
side_level_3_list = pd.Series(all_movements_list[1][2])

x = np.arange(len(labels))  # the label locations

# 01. end-Data preparation

# Set global font and fontsize
font_manager.fontManager.addfont(r'C:\Users\Xingqingjun\AppData\Local\Microsoft\Windows\Fonts\Helvetica.ttf')
plt.rcParams['font.sans-serif'] = 'Helvetica'
plt.rcParams['font.size'] = '16'
width = 0.3  # the width of the bars

fig, ax = plt.subplots(figsize=(10.2, 5.1))

plt.axhline(y=0, ls="-", c="#000000", lw=1)     # Add auxiliary lines in plot.

rects1 = ax.bar(x - width, front_level_1_list, width, color='#2A76A9')
rects2 = ax.bar(x, front_level_2_list, width, color='#F47C34')
rects3 = ax.bar(x + width, front_level_3_list, width, color='#439D47')
#
rects4 = ax.bar(x - width, -side_level_1_list, width, color='#2A76A9', label='[  0.4, 1.0]')
rects5 = ax.bar(x, -side_level_2_list, width, color='#F47C34', label='[  0.1, 0.4)')
rects6 = ax.bar(x + width, -side_level_3_list, width, color='#439D47', label='[0.01, 0.1)')

# Add text for labels, and custom x-axis tick labels.
plt.xlabel("Movements of FMS",labelpad=10.0)
ax.set_ylabel('Frequency (n)')

ax.set_xticks(x)
ax.set_xticklabels(labels)

ax.legend(loc='lower right')
plt.text(15,6, 'Front', rotation=90)
plt.text(15,-13, 'Side', rotation=90)

# Remove the top and bottom borders
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')


fig.tight_layout()

plt.show()
# plt.savefig(pic_save_path, bbox_inches='tight', dpi=300)
# 绘制图——end
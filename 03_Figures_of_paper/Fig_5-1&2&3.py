import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

# the function to calculate percentage.
# the function is used in Fig_5_2 and Fig_5_3.
def func(pct, allvals):
    absolute = int(round(pct/100.*np.sum(allvals)))
    return "{:.1f}%\n".format(pct, absolute)

# 01. start-Data preparation

# the path of XLSX file that the difference information of frame numbers in "Front" and "Side".
xlsx_file_path = r'E:\depth_frames.xlsx'
# the path of saving the file of Fig_5_1.pdf, Fig_5_2.pdf and Fig_5_3.pdf.
pic_save_path = r'E:\Fig_5_1.pdf'

df = pd.read_excel(xlsx_file_path)

# the label of x-axis
row_title_list = df["row_title"]

# the frame number of episodes in "Front" and "Side".
episode_of_depth_front_images_list = df["depth_front"]
episode_of_depth_side_images_list = df["depth_side"]

# the list is used to save the frame number difference of "Front" and "Side".
diff_list = []
# count which part (e1, e2, and e3) has the most episodes of losing frames.
# no_zero_episode_list[0] --- e1, no_zero_episode_list[1] --- e2, no_zero_episode_list[2] --- e3,
no_zero_episode_list = [0, 0, 0]
for i in range(len(episode_of_depth_front_images_list)):
    d_value = episode_of_depth_side_images_list[i] - episode_of_depth_front_images_list[i]
    diff_list.append(d_value)
    if d_value != 0:
        if "_e1" in df["row_title"][i]:
            no_zero_episode_list[0] += 1
        if "_e2" in df["row_title"][i]:
            no_zero_episode_list[1] += 1
        if "_e3" in df["row_title"][i]:
            no_zero_episode_list[2] += 1

# 01. end-Data preparation

# Set global font and fontsize
font_manager.fontManager.addfont(r'C:\Users\Xingqingjun\AppData\Local\Microsoft\Windows\Fonts\Helvetica.ttf')
plt.rcParams['font.sans-serif'] = 'Helvetica'
plt.rcParams['font.size'] = '16'

# # 02_1. start-plot Fig_5_1
#
# fig = plt.figure(figsize=(15.4, 4.8))
#
# plt.axhline(y=0, c="#000", lw=0.5)      # Add auxiliary lines in plot.
# plt.xticks([])
# plt.xlim(-30, 1812 + 30)
# plt.xlabel("Episodes", labelpad=8)
# plt.ylabel("Frames difference")
#
# plt.bar(row_title_list, diff_list, width=2.0)
#
# # Remove the top and bottom borders
# ax = plt.gca()
# ax.spines['right'].set_color('none')
# ax.spines['top'].set_color('none')
#
# # plt.show()
# plt.savefig(pic_save_path, bbox_inches='tight', dpi=300)
#
# # 02_1. end-plot Fig_5_1


# # 02_2. start-plot Fig_5_2
# # group as =0, (0, 5], (5, 10], (10, 30]
# result_list = [0 for i in range(4)]
# for each in diff_list:
#     if each == 0:
#         result_list[0] += 1
#     elif each <= 5:
#         result_list[1] += 1
#     elif each <= 10:
#         result_list[2] += 1
#     elif each <= 30:
#         result_list[3] += 1
#
# fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(aspect="equal"))
#
# color_set = ('#8ED14B', '#3B99D4', '#F06B49', "#ECC2F1")
# wedges, texts, autotexts = ax.pie(result_list, autopct=lambda pct: func(pct, result_list), pctdistance=1.15, colors=color_set)
#
# # the legend text
# ingredients = ["        =0", "(  0,   5]", "(  5, 10]", "(10, 30]"]    # =0, (0, 5], (5, 10], (10, 30]
# # the legend position
# ax.legend(wedges, ingredients,
#           loc="center left",
#           bbox_to_anchor=(1, 0, 0.5, 1))
#
# plt.setp(autotexts, size=20)
#
# plt.show()
# # plt.savefig(pic_save_path, bbox_inches='tight', dpi=300)
#
# # 02_2. end-plot Fig_5_2


# 02_3. start-plot Fig_5_3

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(aspect="equal"))

data = no_zero_episode_list

color_set = ('#3B99D4', '#8ED14B', '#F06B49')
wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data), pctdistance=1.15, colors=color_set)

# the legend text
ingredients = ["e1", "e2", "e3"]
ax.legend(wedges, ingredients, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)

plt.setp(autotexts, size=20)

# plt.show()
plt.savefig(pic_save_path, bbox_inches='tight', dpi=300)

# 02_3. end-plot Fig_5_3



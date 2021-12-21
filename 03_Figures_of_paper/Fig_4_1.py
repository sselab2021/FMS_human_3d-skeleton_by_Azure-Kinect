import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 01. start-Data preparation

# To save the CSV files that recorded the frequency of no-body frames in 'Front' and 'Side' sensors
# Front.csv and Side.csv are saved in dataset.
nobody_csv_file_list = [r'G:\Dataset of FMS\Preprocessing files\Statistics of frames without skeleton\Front.csv',
                        r'G:\Dataset of FMS\Preprocessing files\Statistics of frames without skeleton\Side.csv']

# the path of saving the file of Fig_4_1.
pic_save_path = r'E:\Fig_4_1.pdf'

# Temporarily store the rate of no-body
no_bodies_frames_rate_list = []
for i in range(len(nobody_csv_file_list)):
    df = pd.read_csv(nobody_csv_file_list[i])
    no_bodies_frames_rate_list.append((df["no_bodies_frames_rate"]).tolist())

# 01. end-Data preparation

# 02. start-plot

# Set global font and fontsize
font_manager.fontManager.addfont(r'C:\Users\Xingqingjun\AppData\Local\Microsoft\Windows\Fonts\Helvetica.ttf')
plt.rcParams['font.sans-serif'] = 'Helvetica'
plt.rcParams['font.size'] = '16'

x_data = [i + 1 for i in range(1812)]
y_data = no_bodies_frames_rate_list[0]
y_data2 = no_bodies_frames_rate_list[1]

fig = plt.figure(figsize=(7.2, 5.1))

# Add auxiliary lines in plot.
plt.axhline(y=0.01, ls="--", c="#1B9F2E", lw=0.5)
plt.axvline(x=59, ymin=0, ymax=1 / 22, ls="--", c="green", lw=0.5)
plt.axvline(x=347, ymin=0, ymax=1 / 22, ls="--", c="green", lw=0.5)

# Key marker in plot.
point_x = [59, 347]
point_y = [0.01, 0.01]
point_colors = ["#ff0000", "#1F77B4"]
plt.scatter(point_x, point_y, s=9, c=point_colors)

plt.text(53, 0.05, "(59, 0.01)", fontsize=16)
plt.text(341, 0.05, "(347, 0.01)", fontsize=16)

# Remove the top and bottom borders
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

ln1, = plt.plot(x_data, y_data, color='red', linewidth=2.0)
ln2, = plt.plot(x_data, y_data2, linewidth=2.0)

x = range(0, 1813, 300)
plt.xticks(x)
plt.xlim(-50, 1812)
plt.xlabel("Number of episodes (N)", labelpad=10.0)
plt.ylabel("No-body frame ratios (%)")

plt.legend(handles=[ln1, ln2], labels=['Front', 'Side'])

# plt.show()
plt.savefig(pic_save_path, bbox_inches='tight', dpi=300)

# 02. end-plot

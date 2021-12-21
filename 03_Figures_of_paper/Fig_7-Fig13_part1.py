"""
    # Fig_X_x (movementID, jointIndex)
    # this .py script is suitable for movements and joints as follows:
        Fig_7_1 (m01, 18), Fig_7_3 (m02, 18)
        Fig_8_1 (m03, 19)
        Fig_9_1 (m05, 18)
        Fig_10_1 (m07, 7)
        Fig_11_1 (m09, 20)
        Fig_12_1 (m11, 3)
        Fig_13_1 (m12, 20)
        Fig_13_3 (m14, 24)
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from matplotlib import font_manager
from scipy import signal
from scipy import stats


# the path of all skeleton data (Front)
all_json_files_path = r'G:\202106FMS_data\Dataset of FMS\Skeleton data\Front'
# the path of file "expert score.json"
expert_score_json_file = r'G:\202106FMS_data\Dataset of FMS\experts_score.json'

# the path of saving the file of Fig_4_1.
pic_save_path = r'G:\Fig_X_x.pdf'

# 01. start-Data preparation

# separate store the skeleton data file to the list by movement category.
all_movement_files_list = [[] for i in range(15)]
all_json_files_list = os.listdir(all_json_files_path)
for index, per_json in enumerate(all_json_files_list):
    movementID = int(per_json.split("_")[2][1:])
    all_movement_files_list[movementID - 1].append(per_json)

# read the file "experts_score.json"
with open(expert_score_json_file) as json_f:
    expert_score_json_dict = json.load(json_f)

# the list is used to save the valid frame number of all episodes in the path "all_json_files_path".
# prepare for time series normalization.
episodes_valid_frames_list = []
valid_episodes_json_files_list = []
episodes_expert_scores_list = []

# data extraction according to the index of movements.
for index, each_json in enumerate(all_movement_files_list[13]):     # all_movement_files_list[0] represents m01, all_movement_files_list[1] represents m02 and so on.
    per_json_path = os.path.join(all_json_files_path, each_json)
    with open(per_json_path) as json_f:
        json_dict = json.load(json_f)

    # Filter out the files of having many no-body frame number (r>0.9)
    have_body_frame_num = json_dict["total_frames"]
    for i in range(json_dict["total_frames"]):
        if json_dict["frames"][i]["num_bodies"] == 0:
            have_body_frame_num -= 1
    if have_body_frame_num / json_dict["total_frames"] <= 0.9:
        continue

    episodes_valid_frames_list.append(have_body_frame_num)
    valid_episodes_json_files_list.append(each_json)

    subjectID = each_json.split("_")[1]
    movementID = each_json.split("_")[2]
    episodeID = each_json.split("_")[-1].split(".")[0]

    # take the average value of expert scores of one episode.
    # add this value to "episodes_expert_scores_list"
    episode_score = round(np.mean(expert_score_json_dict[subjectID][movementID][episodeID]))
    episodes_expert_scores_list.append(episode_score)

# the average value of all episodes in the movement. Results rounded
episodes_frame_avg = int(np.mean(episodes_valid_frames_list))

# the list is used to save the x, y, and z coordinate values of one joint.
joint_xyz_values_list = [[[], [], []] for i in range(len(valid_episodes_json_files_list))]

# the initialization of x-label.
label_x_new = np.empty((0, 1))

for index, per_json in enumerate(valid_episodes_json_files_list):
    per_json_path = os.path.join(all_json_files_path, per_json)
    with open(per_json_path) as json_f:
        json_dict = json.load(json_f)

    for i in range(json_dict["total_frames"]):
        if json_dict["frames"][i]["num_bodies"] == 0:
            continue
        # json_dict["frames"][i]["bodies"][0]["joint_positions"][index] "index" is the index of joints
        joint_x_values = json_dict["frames"][i]["bodies"][0]["joint_positions"][23][0]      # the x-value of 23th joint
        joint_y_values = json_dict["frames"][i]["bodies"][0]["joint_positions"][23][1]      # the y-value of 23th joint
        joint_z_values = json_dict["frames"][i]["bodies"][0]["joint_positions"][23][2]      # the z-value of 23th joint

        joint_xyz_values_list[index][0].append(joint_x_values)
        joint_xyz_values_list[index][1].append(-joint_y_values)     # the y-value is reverse
        joint_xyz_values_list[index][2].append(joint_z_values)

    x_ = [i for i in range(episodes_valid_frames_list[index])]

    # step1-filtering
    b, a = signal.butter(8, 0.07, 'lowpass')
    joint_xyz_values_list[index][0] = signal.filtfilt(b, a, joint_xyz_values_list[index][0])
    joint_xyz_values_list[index][1] = signal.filtfilt(b, a, joint_xyz_values_list[index][1])
    joint_xyz_values_list[index][2] = signal.filtfilt(b, a, joint_xyz_values_list[index][2])

    # step2-Interpolation processing
    li_x = interp1d(x_, joint_xyz_values_list[index][0], kind='cubic')
    li_y = interp1d(x_, joint_xyz_values_list[index][1], kind='cubic')
    li_z = interp1d(x_, joint_xyz_values_list[index][2], kind='cubic')

    label_x_new = np.linspace(0, episodes_valid_frames_list[index] - 1, episodes_frame_avg)

    joint_xyz_values_list[index][0] = li_x(label_x_new)
    joint_xyz_values_list[index][1] = li_y(label_x_new)
    joint_xyz_values_list[index][2] = li_z(label_x_new)

# step3-normalization
# the list is used to save the x, y, and z coordinate values (Filtered and interpolated)
single_joint_xyz_set_list = [[], [], []]
for i in range(len(valid_episodes_json_files_list)):
    single_joint_xyz_set_list[0].append(joint_xyz_values_list[i][0])
    single_joint_xyz_set_list[1].append(joint_xyz_values_list[i][1])
    single_joint_xyz_set_list[2].append(joint_xyz_values_list[i][2])

single_joint_xyz_set_list[0] = stats.zscore(single_joint_xyz_set_list[0], axis=1, ddof=1)
single_joint_xyz_set_list[1] = stats.zscore(single_joint_xyz_set_list[1], axis=1, ddof=1)
single_joint_xyz_set_list[2] = stats.zscore(single_joint_xyz_set_list[2], axis=1, ddof=1)

label_x_new = (episodes_frame_avg / (episodes_valid_frames_list[index] - 1)) * label_x_new

# 01. end-Data preparation

# 02. start-plot

# Set global font and fontsize
font_manager.fontManager.addfont(r'C:\Users\Xingqingjun\AppData\Local\Microsoft\Windows\Fonts\Helvetica.ttf')
plt.rcParams['font.sans-serif'] = 'Helvetica'
plt.rcParams['font.size'] = '16'

fig = plt.figure()
# according to the experts' scores, the curves are in different colors
for i in range(len(valid_episodes_json_files_list)):
    if episodes_expert_scores_list[i] == 1:
        color_ = '#3B99D4'
    if episodes_expert_scores_list[i] == 2:
        color_ = '#F06B49'
    if episodes_expert_scores_list[i] == 3:
        color_ = '#8ED14B'
    plt.plot(label_x_new, single_joint_xyz_set_list[1][i], color=color_, lw=0.7)

plt.xlabel("Normalized time [frames]",labelpad=10.0)
plt.ylabel("Normalized y-axis")
plt.xlim(0, episodes_frame_avg)

# plt.show()
plt.savefig(pic_save_path, bbox_inches='tight', dpi=300, pad_inches=0.1)

# 02. end-plot
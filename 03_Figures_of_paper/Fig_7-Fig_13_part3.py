"""
    # Fig_X_x (movementID, [a, b, c, d])
    # this .py script is suitable for movements and joints as follows:
        Fig_11_2 (m09, [18, 20, 0, 3])
        Fig_12_2 (m11, [1, 3]) #
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
for index, each_json in enumerate(all_movement_files_list[8]):       # all_movement_files_list[0] represents m01, all_movement_files_list[1] represents m02 and so on.
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
angle_list = [[] for i in range(len(valid_episodes_json_files_list))]

# the initialization of x-label.
label_x_new = np.empty((0, 1))

for index, per_json in enumerate(valid_episodes_json_files_list):
    per_json_path = os.path.join(all_json_files_path, per_json)
    with open(per_json_path) as json_f:
        json_dict = json.load(json_f)

    for i in range(json_dict["total_frames"]):
        if json_dict["frames"][i]["num_bodies"] == 0:
            continue

        # ∠
        # the joints in test limb
        joint_1_xyz = np.array(json_dict["frames"][i]["bodies"][0]["joint_positions"][18])  # a
        joint_2_xyz = np.array(json_dict["frames"][i]["bodies"][0]["joint_positions"][20])  # b
        # the joints in plane
        joint_3_xyz = np.array(json_dict["frames"][i]["bodies"][0]["joint_positions"][0])   # c
        joint_4_xyz = np.array(json_dict["frames"][i]["bodies"][0]["joint_positions"][2])   # d

        # the vectors of above three joints.
        vector1 = joint_2_xyz - joint_1_xyz
        vector2 = joint_4_xyz - joint_3_xyz     # Fig_11_2 m09 Active straight raise
        # Vector2 = (1, 0, 0)   # Fig_12_2 m11 Trunk stability

        # the norm of vectors
        norm_vector1 = np.sqrt(vector1.dot(vector1))
        norm_vector2 = np.sqrt(vector2.dot(vector2))
        # the dot product of vectors
        dot_product = vector1.dot(vector2)
        # the radians of the angle
        angle_cos = dot_product / (norm_vector1 * norm_vector2)
        # convert to an angle value
        angle_deg = (np.arccos(angle_cos) * 180) / np.pi

        angle_list[index].append(angle_deg)


    x_ = [i for i in range(episodes_valid_frames_list[index])]

    # step1-filtering
    b, a = signal.butter(8, 0.07, 'lowpass')
    angle_list[index] = signal.filtfilt(b, a, angle_list[index])

    # step2-Interpolation processing
    li_angle = interp1d(x_, angle_list[index], kind='cubic')

    label_x_new = np.linspace(0, episodes_valid_frames_list[index] - 1, episodes_frame_avg)
    angle_list[index] = li_angle(label_x_new)

label_x_new = (episodes_frame_avg / (episodes_valid_frames_list[index] - 1)) * label_x_new

# 01. end-Data preparation

# 02. start-plot

# Set global font and fontsize
font_manager.fontManager.addfont(r'C:\Users\Xingqingjun\AppData\Local\Microsoft\Windows\Fonts\Helvetica.ttf')
plt.rcParams['font.sans-serif'] = 'Helvetica'
plt.rcParams['font.size'] = '16'

fig = plt.figure()
for i in range(len(valid_episodes_json_files_list)):
    if episodes_expert_scores_list[i] == 1:
        color_ = '#3B99D4'
    if episodes_expert_scores_list[i] == 2:
        color_ = '#F06B49'
    if episodes_expert_scores_list[i] == 3:
        color_ = '#8ED14B'
    plt.plot(label_x_new, angle_list[i], color=color_, lw=0.7)

plt.xlabel("Normalized time [frames]",labelpad=10.0)
plt.ylabel("Flexion / extension [degrees]")
plt.xlim(0, episodes_frame_avg)

# plt.show()
plt.savefig(pic_save_path, bbox_inches='tight', dpi=300, pad_inches=0.1)

# 02. end-plot
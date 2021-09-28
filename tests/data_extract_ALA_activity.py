"""
wATR, woATRのディレクトリ直下で実行
stimのデータを抽出してまとめる
"""

import os
import re
import numpy as np
import pandas
import tkinter
from tkinter import filedialog
from tkinter import messagebox

import pandas as pd


def ask_dir_name():
    root = tkinter.Tk()
    root.withdraw()
    messagebox.showinfo('select directory', 'select analyzing directory')
    directory = filedialog.askdirectory()
    os.chdir(directory)


def search_subdivided_dir_path():
    """
    extract the Stimuli_**.csv paths from selected directory
    :return
    stimuli_data_list: list, path of csv files, full path
    date_list: list, analysis date list, for making directories
    """
    date_list = []
    stimuli_data_list = []
    for curDir, dirs, files in os.walk("./"):
        for file in files:
            if len(curDir.split("\\")) !=1:
                pre_date_list = [i for i in curDir.split("\\") if re.match("analyzed_data_\d+-\d+-\d+", i)]
                if pre_date_list:
                    date = pre_date_list[0].split("_")[-1]
                    if date in date_list:
                        pass
                    else:
                        date_list.append(date)
                else:
                    pass
            if os.path.basename(file).split("_")[0] == "Stimuli":
                stimuli_data_list.append(os.path.join(curDir, file))
            else:
                pass
    return stimuli_data_list, date_list


def data_extraction_and_summarize(stimuli_data_list, date_list):
    data_dict = {}
    for path in stimuli_data_list:
        # get date
        current_data_analyzed_date_list = [i for i in path.split("\\") if re.match("analyzed_data_\d+-\d+-\d+", i)]
        if current_data_analyzed_date_list:
            current_data_analyzed_date = current_data_analyzed_date_list[0].split("_")[-1]
        else:
            pass
        # get experiment name
        current_data_experiment_name_list = [i for i in path.split("\\") if re.match("\d+_remEx\.+", i)]
        if current_data_experiment_name_list:
            current_data_experiment_name = current_data_experiment_name_list[0]
        else:
            pass
        # get stimuli number
        current_stimuli_number = path.split("\\")[-1].split("_")[-1]

        # make destination directory
        os.makedirs("./extracted_data/{}".format(current_data_analyzed_date), exist_ok=True)

        # get data
        current_data_array = pd.read_csv(path).values

        # add data
        if current_data_analyzed_date in data_dict:
            saved_df = data_dict[current_data_analyzed_date]
            saved_df[current_data_experiment_name] = current_data_array
        else:


    """is_labels_MQ = [[0] for i in range(len(date_list))]
    is_labels_QM = [[0] for i in range(len(date_list))]
    MQ_labels = [[0] for i in range(len(date_list))]
    QM_labels = [[0] for i in range(len(date_list))]
    # make directories
    os.makedirs("./extracted_data", exist_ok=True)
    # MQ data extraction
    # initiation the data list
    island_MQ_data = [[0] for i in range(len(date_list))]
    all_MQ_data = [[0] for i in range(len(date_list))]
    for path in MQ_list:
        # check directory type, island? MQ?
        dir_type = path.split("\\")[-2]
        Ex_date = [i for i in path.split("\\") if re.match("Ex-\d+_date_\d+-\d+-\d+", i)][0].split("_")[-1]
        # index of Ex_date
        index_of_date = date_list.index(Ex_date)
        os.makedirs("./extracted_data/{}".format(Ex_date), exist_ok=True)
        data = pd.read_csv(path)
        if re.match("island\d+", dir_type):
            temp_array = data["deltaF/F"].values
            if len(island_MQ_data[index_of_date]) == 1:
                island_MQ_data[index_of_date] = temp_array
            else:
                island_MQ_data[index_of_date]  = np.vstack((island_MQ_data[index_of_date],
                                                            temp_array))
            # island_MQ_data.append(temp_array)
            if len(all_MQ_data[index_of_date]) == 1:
                all_MQ_data[index_of_date] = temp_array
            else:
                all_MQ_data[index_of_date] = np.vstack((all_MQ_data[index_of_date], temp_array))
            # all_MQ_data.append(temp_array)
            is_labels_MQ[index_of_date].append("MQ_" + path.split("\\")[1] + "_" + path.split("\\")[-2])
            MQ_labels[index_of_date].append("MQ_" + path.split("\\")[1] + "_" + path.split("\\")[-2])
        # MQ tr data
        else:
            temp_array = data["deltaF/F"].values
            if len(all_MQ_data[index_of_date]) == 1:
                all_MQ_data[index_of_date] = temp_array
            else:
                all_MQ_data[index_of_date] = np.vstack((all_MQ_data[index_of_date], temp_array))
            # all_MQ_data.append(temp_array)
            MQ_labels[index_of_date].append("MQ_" + path.split("\\")[1] + "_" + path.split("\\")[-2])
    # make dataframes
    for i in range(len(date_list)):
        island_MQ_df = pd.DataFrame(np.array(island_MQ_data[i]).T, columns=is_labels_MQ[i][1:])
        all_MQ_df = pd.DataFrame(np.array(all_MQ_data[i]).T, columns=MQ_labels[i][1:])
    # save
        island_MQ_df.to_csv("./extracted_data/{}/island_MQ.csv".format(date_list[i]))
        all_MQ_df.to_csv("./extracted_data/{}/all_MQ.csv".format(date_list[i]))

    # QM data extraction
    island_QM_data = [[0] for i in range(len(date_list))]
    all_QM_data = [[0] for i in range(len(date_list))]
    for path in QM_list:
        dir_type = path.split("\\")[-2]
        Ex_date = [i for i in path.split("\\") if re.match("Ex-\d+_date_\d+-\d+-\d+", i)][0].split("_")[-1]
        os.makedirs("./extracted_data/{}".format(Ex_date), exist_ok=True)
        index_of_date = date_list.index(Ex_date)
        data = pd.read_csv(path)
        if re.match("island\d+", dir_type):
            temp_array = data["deltaF/F"].values
            if len(island_QM_data[index_of_date]) == 1:
                island_QM_data[index_of_date] = temp_array
            else:
                island_QM_data[index_of_date] = np.vstack((island_QM_data[index_of_date], temp_array))
            # island_MQ_data.append(temp_array)
            if len(all_QM_data[index_of_date]) == 1:
                all_QM_data[index_of_date] = temp_array
            else:
                all_QM_data[index_of_date] = np.vstack((all_QM_data[index_of_date], temp_array))
            is_labels_QM[index_of_date].append("QM_" + path.split("\\")[1] + "_" + path.split("\\")[-2])
            QM_labels[index_of_date].append("QM_" + path.split("\\")[1] + "_" + path.split("\\")[-2])
        else:
            temp_array = data["deltaF/F"].values
            if len(all_QM_data[index_of_date]) == 1:
                all_QM_data[index_of_date] = temp_array
            else:
                all_QM_data[index_of_date] = np.vstack((all_QM_data[index_of_date], temp_array))
            # all_MQ_data.append(temp_array)
            QM_labels[index_of_date].append("QM_" + path.split("\\")[1] + "_" + path.split("\\")[-2])

    for i in range(len(date_list)):
        island_QM_df = pd.DataFrame(np.array(island_QM_data[i]).T, columns=is_labels_QM[i][1:])
        all_QM_df = pd.DataFrame(np.array(all_QM_data[i]).T, columns=QM_labels[i][1:])
    # save
        island_QM_df.to_csv("./extracted_data/{}/island_QM.csv".format(date_list[i]))
        all_QM_df.to_csv("./extracted_data/{}/all_QM.csv".format(date_list[i]))"""


def main():
    ask_dir_name()
    stimuli_data_list, date_list = search_subdivided_dir_path()
    data_extraction_and_summarize(stimuli_data_list, date_list)


if __name__ == '__main__':
    main()

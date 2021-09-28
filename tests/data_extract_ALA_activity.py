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
        current_data_name = current_data_experiment_name + "Stimuli_" + current_stimuli_number

        # add data
        if current_data_analyzed_date in data_dict:
            saved_df = data_dict[current_data_analyzed_date]
            saved_df[current_data_name] = current_data_array
        else:
            data_dict[current_data_analyzed_date] = pd.DataFrame(current_data_array,
                                                                 columns=current_data_name)

    for key in data_dict:
        data = data_dict[key]
        data.to_csv("./extracted_data/{}".format(key))


def main():
    ask_dir_name()
    stimuli_data_list, date_list = search_subdivided_dir_path()
    data_extraction_and_summarize(stimuli_data_list, date_list)


if __name__ == '__main__':
    main()

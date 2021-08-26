import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import tkinter
from tkinter import messagebox
from tkinter import filedialog

stimuli_list = [1775, 2610, 3745, 4326]
threshold = 80
Shortest_M_bout_duration = 5

def select_file():
    root = tkinter.Tk()
    root.withdraw()
    messagebox.showinfo('select file', 'select file')
    path = filedialog.askopenfilename()
    dir_path = os.path.dirname(path)
    os.chdir(dir_path)
    os.makedirs("./dfs", exist_ok=True)
    os.makedirs("./figs", exist_ok=True)
    return path


def duration_analysis(data, stimulated_frame):
    extracted_data = data[stimulated_frame:].iloc[:, 1].values
    if extracted_data[0] != 1:
        motion_duration = 0
    else:
        motion_duration = np.argmin(extracted_data) / 2
    return motion_duration


def analysis(path, stimuli_list):
    data = pd.read_csv(path)
    timeaxis = data.iloc[:, 0] * 0.5

    # make activity graphs
    plt.plot(data.iloc[:, 1], color="black")
    plt.ylim(0, 1000)
    plt.savefig("./figs/activity_plot.png")

    # make M Q graph
    motion_data = data.iloc[:, 1].values
    MorQ = np.where(motion_data > threshold, 1, 0)
    plt.plot(MorQ, color="black")
    plt.savefig("./figs/MorQ.png")

    # calc motion and make graphs
    tempstart = 0
    motion = np.zeros(len(timeaxis))
    for i in np.where(motion_data > threshold)[0]:
        timeduration = float(timeaxis[i] - timeaxis[tempstart])
        if timeduration < Shortest_M_bout_duration:
            motion[tempstart:i] = 1
        else:
            pass
        tempstart = i
    plt.plot(motion, color="black")
    plt.savefig("./figs/motion_bout_fig.png")
    timeaxis_array = timeaxis.values
    motion_bout_df = pd.DataFrame(np.vstack([timeaxis_array, motion]).T, columns=["time", "motion_bout"])
    motion_bout_df.to_csv("./dfs/motion_bout_df.csv", index=False)

    motion_duration_list = []
    for i in range(len(stimuli_list)):
        motion_duration_list.append(duration_analysis(motion_bout_df, stimuli_list[i]))
    motion_duration_df = pd.DataFrame(np.vstack((stimuli_list, motion_duration_list)).T,
                                      columns=["stimuli timing", "motion_duration (sec)"])
    motion_duration_df.to_csv("./dfs/motion_duration_df.csv")


def main():
    path = select_file()
    analysis(path, stimuli_list)


if __name__ == '__main__':
    main()

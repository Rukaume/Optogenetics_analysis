# -*- coding: utf-8 -*-
"""

"""

import cv2
import datetime
import os
import os.path
import sys
import time
import tkinter
from tkinter import filedialog
from tkinter import messagebox

import numpy as np
import pandas as pd
from PIL import Image
from numpy import ndarray
from skimage.color import rgb2gray
from skimage import io
from skimage import io, img_as_float, img_as_ubyte
from tqdm import tqdm
from skimage.filters.rank import median
from skimage.morphology import disk

# parameters
threshold = 5


def get_image_filelist():
    root = tkinter.Tk()
    root.withdraw()
    # initial directory
    messagebox.showinfo('selectfiles', 'select analyzing image')
    image_file_path = tkinter.filedialog.askopenfilename()
    image_directory = os.path.dirname(image_file_path)
    if image_file_path == "":
        messagebox.showinfo('cancel', 'stop before image setting')
        sys.exit()
    os.chdir(image_directory)
    filelist = os.listdir('.')
    filelist = [i for i in filelist if os.path.splitext(i)[1] == '.jpg' \
                or os.path.splitext(i)[1] == '.png' \
                or os.path.splitext(i)[1] == ".tiff" \
                or os.path.splitext(i)[1] == ".tif"]
    return filelist


def data_select():
    file_list: list[str] = get_image_filelist()
    number_of_images: int = len(file_list) - 1
    if number_of_images < 100:
        messagebox.showinfo('cancel', 'there are not enough amount of images')
    else:
        pass
    return file_list, number_of_images


def threshold_set(file_list, number_of_images):
    sampling_cycle = (number_of_images // 100) - 1
    threshold_list = []
    for p in tqdm(range(100)):
        sample_num = p * sampling_cycle
        sample_path = file_list[sample_num]
        next_to_sample_path = file_list[sample_num + 1]
        sample_img = rgb2gray(img_as_float(io.imread(sample_path)))
        sample_img2 = rgb2gray(img_as_float(io.imread(next_to_sample_path)))
        if p == 0:
            sample_subtract_img = cv2.absdiff(sample_img, sample_img2)
        else:
            sub = cv2.absdiff(sample_img, sample_img2)
            sample_subtract_img = np.vstack([sample_subtract_img, sub])
    sample_mean = sample_subtract_img.mean()
    sample_std = sample_subtract_img.std()
    threshold_pixel = threshold * sample_std + sample_mean

    return threshold_pixel


def image_subtraction_analysis(file_list, threshold_pixel):
    t1 = time.time()
    data_list: list = []
    for n in tqdm(range(len(file_list) - 1)):
        img1_path = file_list[n]
        img2_path = file_list[(int(n) + 1)]

        img1: ndarray = rgb2gray(img_as_float(io.imread(img1_path)))
        img2: ndarray = rgb2gray(img_as_float(io.imread(img2_path)))
        subtracted_image = cv2.absdiff(img1,img2)
        data_list.append(np.count_nonzero(subtracted_image > threshold_pixel))
    data_array = np.array(data_list)
    t2 = time.time()
    elapsed_time = t2 - t1
    print(f"経過時間：{elapsed_time}")
    return data_array, elapsed_time


def data_save(data_list, elapsed_time):
    s = pd.DataFrame(data_list)
    s_name = os.path.basename("./")

    date = datetime.date.today()
    time = datetime.datetime.now()
    os.chdir('../')
    os.makedirs('./analyzed_data_{}'.format(date), exist_ok=True)
    os.chdir('./analyzed_data_{}'.format(date))
    s.to_csv('./locomotor_activity_th={0}.csv'.format(threshold))
    path_w = './readme.txt'
    contents = '\nanalyzed_date: {0}\nelapsed time: {1}\nthreshold: {2}'.format(time,
                                                                                elapsed_time,
                                                                                threshold)

    with open(path_w, mode="a") as f:
        f.write(contents)


def main():
    file_list, number_of_images = data_select()
    threshold_pixel = threshold_set(file_list, number_of_images)
    data_array, elapsed_time = image_subtraction_analysis(file_list, threshold_pixel)
    data_save(data_array, elapsed_time)
    sys.exit()


if __name__ == '__main__':
    main()

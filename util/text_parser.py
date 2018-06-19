# -*- coding: utf-8 -*-

import os

folder_list = []


def traverse(f):
    fs = os.listdir(f)
    for f1 in fs:
        tmp_path = os.path.join(f, f1)
        if os.path.isdir(tmp_path):
            folder_list.append(tmp_path)


def get_all_files(f):
    fs = os.listdir(f)
    file_list = []
    for f1 in fs:
        tmp_path = os.path.join(f, f1)
        if not os.path.isdir(tmp_path):
            file_list.append(tmp_path)
    return file_list


def get_all_enwiki_files(path):
    traverse(path)
    all_files = []
    for folder in folder_list:
        all_files.append(get_all_files(folder))

    print(all_files)


path = 'E:\\bishe\\wikiProject\\enwik'
get_all_enwiki_files(path)

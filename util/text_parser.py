# -*- coding: utf-8 -*-

import os
import re
from db.model import Wikipedia
from db.model import EngineFactory
from sqlalchemy import insert
from db.sql_handler import SQLHandler
import sys

folder_list = []
session = EngineFactory.create_session()
sql_handler = SQLHandler()


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
    return all_files


# def parse_file
def get_id_url_title(line):
    wiki_id = 0
    url = ''
    title = ''
    pattern1 = re.compile(r'id="(.*?)"')
    result1 = pattern1.findall(line)
    if len(result1) > 0:
        wiki_id = result1[0]

    pattern2 = re.compile(r'url="(.*)" ')
    result2 = pattern2.findall(sline)
    if len(result2) > 0:
        url = result2[0]
    pattern3 = re.compile(r'title="(.*)">')
    result3 = pattern3.findall(sline)
    if len(result3) > 0:
        title = result3[0]

    return wiki_id, url, title


path = '/home/fdse/data_prepare/wikipedia/wikiextractor/enwiki'
content = ''
wiki_id = 0
url = ''
title = ''
all_files = get_all_enwiki_files(path)
for filenames in all_files:
    for file in filenames:
        print(file)
        for line in open(file):
            sline = line
            if sline == '':
                continue
            else:
                if sline.find('<doc id="') == 0:
                    content = ''
                    wiki_id, url, title = get_id_url_title(sline)
                elif sline.find('</doc>') == 0:
                    sql_handler.add_wikipedia(wiki_id, url, title, content)
                    print(content)
                    wiki_id = 0
                    url = ''
                    title = ''
                    content = ''
                else:
                    content += sline

# line = '<doc id="56569671" url="https://en.wikipedia.org/wiki?curid=56569671" title="Shift (1982 film)">'
# sline = line.strip()
#
# pattern1 = re.compile(r'id="(.*?)"')
# result1 = pattern1.findall(sline)
# print(result1[0])
#
# pattern2 = re.compile(r'url="(.*)" ')
# result2 = pattern2.findall(sline)
# print(result2[0])
#
# pattern2 = re.compile(r'title="(.*)">')
# result2 = pattern2.findall(sline)
# print(result2[0])

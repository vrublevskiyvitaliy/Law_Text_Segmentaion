# coding=utf-8
from os import listdir
from os.path import isfile, join
from StructuredText import StructuredText
txt_path = 'txt_from_html/'
list_path = 'lists/'


def find_title():
    #files_txt = [f for f in listdir(txt_path) if isfile(join(txt_path, f)) and f[-3:] == 'txt']
    #files_txt = files_txt[:1]
    files_txt = ['1AXOw9oDa18zA7ZvTymzzi.txt']
    for file in files_txt:
        txt_before_path = txt_path + file
        text = StructuredText(txt_before_path)
        cand = text.find_lists()
        text.write_list_to_file(list_path + file[:-3] + 'html')


find_title()
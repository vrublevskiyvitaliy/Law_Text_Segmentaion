import docx2txt
import os
from os import listdir
from os.path import isfile, join
import json
documents_path = 'documents/'


def add_to_bad_docx(list):
    with open('bad_docx.json') as data_file:
        data = json.load(data_file)

    for item in list:
        data.append(item)

    data = list(set(data))

    with open('bad_docx.json', 'w') as outfile:
        json.dump(data, outfile)


def filter_docx():
    files_docx = [f for f in listdir(documents_path) if isfile(join(documents_path, f)) and f[-4:] == 'docx']

    filtered = 0
    list = []
    for file in files_docx:
        docx_path = documents_path + file
        try:
            a = docx2txt.process(docx_path).encode('utf-8')
        except Exception as e:
            print(file)
            list.append(file)
            os.remove(docx_path)
            filtered += 1
    print(str(filtered))
    add_to_bad_docx(list)

filter_docx()
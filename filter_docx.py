import docx2txt
import os
from os import listdir
from os.path import isfile, join

documents_path = 'documents/'


def filter_docx():
    files_docx = [f for f in listdir(documents_path) if isfile(join(documents_path, f)) and f[-4:] == 'docx']

    for file in files_docx:
        docx_path = documents_path + file
        try:
            a = docx2txt.process(docx_path).encode('utf-8')
        except Exception as e:
            print(file)
            os.remove(docx_path)

filter_docx()
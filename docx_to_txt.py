import docx2txt
from os import listdir
from os.path import isfile, join

documents_path = 'documents/'
txt_path = 'txt/'


def convert_docx_to_txt():
    files_docx = [f for f in listdir(documents_path) if isfile(join(documents_path, f)) and f[-4:] == 'docx']

    for file in files_docx:
        docx_path = documents_path + file
        print docx_path
        path = txt_path + file[:-4] + 'txt'
        try:
            a = docx2txt.process(docx_path).encode('utf-8')
            f = open(path, 'w')
            f.write(a)
        except Exception as e:
            print('Error')


convert_docx_to_txt()
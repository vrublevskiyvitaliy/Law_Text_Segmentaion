# coding=utf-8
from os import listdir
from os.path import isfile, join
from StructuredText import StructuredText
path = 'documents/'
#path = 'txt_from_html/'
#path = 'Lawyer Test/'
list_path = 'lists/'
#extencion = 'txt'
extencion = 'docx'

def find_list():
    files = [f for f in listdir(path) if isfile(join(path, f)) and f.split('.')[1] == extencion]
    #files_txt = files_txt[:1]
    # files = ['retainer-agreement.txt']
    # files = ['power-of-attorney.txt']
    # files = ['contract-for-mobile-application-development-services.txt']
    # files = ['1BdeYqcvvjtH306sk9gXX3.txt']
    # files = ['1AXOw9oDa18zA7ZvTymzzi.txt']
    files = ['14tsEF5dHpm8B2kKm0TbpP.docx']
    #files = files[:10]
    #files = files[:10]
    # files = ['rental-agreement-plain-language-lease.txt']
    for file in files:
        file_id = file.split('.')[0]
        file_path = path + file
        text = StructuredText(file_path)
        text.find_lists()
        text.write_group_lists_structure(list_path + file_id + '.html')
        text.analyze_list_structure()
        print text.sections
        print 'file:///Users/vitaliyvrublevskiy/projects/text_segmentation/lists/' + file_id + '.html'

find_list()
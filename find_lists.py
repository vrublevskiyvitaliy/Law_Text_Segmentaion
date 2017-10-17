# coding=utf-8
from os import listdir
from os.path import isfile, join
from StructuredText import StructuredText
path = 'txt_from_html/'
#path = 'Lawyer Test/'
list_path = 'lists/'
extencion = 'txt'
#extencion = 'doc'

def find_list():
    files = [f for f in listdir(path) if isfile(join(path, f)) and f[-3:] == extencion]
    #files_txt = files_txt[:1]
    files = ['retainer-agreement.txt']
    files = ['power-of-attorney.txt']
    files = ['contract-for-mobile-application-development-services.txt']
    files = ['1BdeYqcvvjtH306sk9gXX3.txt']
    #files = ['1AXOw9oDa18zA7ZvTymzzi.txt']
    #files = ['1CSIxpTpXxAiAQ0ilodA8X.txt']
    # files = ['rental-agreement-plain-language-lease.txt']
    for file in files:
        file_path = path + file
        text = StructuredText(file_path)
        text.find_lists()
        text.write_group_lists_structure(list_path + file[:-3] + 'html')
        text.analyze_list_structure()
        print text.sections
        print 'file:///Users/vitaliyvrublevskiy/projects/text_segmentation/lists/' + file[:-3] + 'html'

find_list()
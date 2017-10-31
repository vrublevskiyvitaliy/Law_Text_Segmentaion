# coding=utf-8
from os import listdir
from os.path import isfile, join
from StructuredText import StructuredText
import json

path = 'documents/'
parsed_path = 'parsed/'

# path = 'txt_from_html/'
#path = 'Lawyer Test/'
list_path = 'lists/'
#extencion = 'txt'
extencion = 'docx'


def filter_section(s):
    return len(s) < 100


def add_sections(sections):
    flag = True
    for s in sections:
        if not filter_section(s):
            flag = False

    if not flag:
        print "Too long"
        return

    with open('sections.json') as data_file:
        data = json.load(data_file)

    for item in sections:
        s = item.lower().strip('.')
        if len(s) > 0:
            data.append(s)

    data = list(set(data))

    with open('sections.json', 'w') as outfile:
        json.dump(data, outfile)


def print_sections(sections):
    for s in sections:
        print s


def find_list():
    files = [f for f in listdir(path) if isfile(join(path, f)) and f.split('.')[1] == extencion]
    # files = ['retainer-agreement.txt']
    # files = ['power-of-attorney.txt']
    # files = ['contract-for-mobile-application-development-services.txt']
    # files = ['1BdeYqcvvjtH306sk9gXX3.txt']
    files = ['1AXOw9oDa18zA7ZvTymzzi.docx']
    #files = ['1gSpQJeKuF8YWFRwu8UmvZ.docx']
    #files = ['14tsEF5dHpm8B2kKm0TbpP.docx']
    #files = files[:30]
    #files = files[:10]
    # files = ['rental-agreement-plain-language-lease.txt']
    for file in files:
        print '*********************************'
        file_id = file.split('.')[0]
        print 'ID ' + file_id
        file_path = path + file
        text = StructuredText(file_path)
        text.find_lists()
        text.write_group_lists_structure(list_path + file_id + '.html')
        text.save_parsed(parsed_path + file_id + '.txt')
        text.analyze_list_structure()
        print_sections(text.sections)
        add_sections(text.sections)
        print 'file:///Users/vitaliyvrublevskiy/projects/text_segmentation/lists/' + file_id + '.html'


find_list()
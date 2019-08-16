import docx2txt
import os
from os import listdir
from os.path import isfile, join
import json


def filter_section():
    with open('all_sections.json') as data_file:
        data = json.load(data_file)

    filtered_data = []

    for s in data:
        if len(s['section_full_title']) < 110:
            filtered_data.append(s)

    filtered_data = filtered_data[:100]
    with open('all_sections_filtered_limited_100.json', 'w') as outfile:
        json.dump(filtered_data, outfile)

filter_section()
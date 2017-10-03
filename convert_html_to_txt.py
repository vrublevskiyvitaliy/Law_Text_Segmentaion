import os
import json
from bs4 import BeautifulSoup

path_to_dataset = '/Users/vitaliyvrublevskiy/contracts_2010'


def find_files(files, dirs, extensions):
    new_dirs = []
    for d in dirs:
        try:
            new_dirs += [os.path.join(d, f) for f in os.listdir(d)]
        except OSError:
            if os.path.splitext(d)[1] in extensions:
                files.append(d)

    if new_dirs:
        find_files(files, new_dirs, extensions)
    else:
        return


def generate_combined_meta_data(files):
    json_data = []

    for f in files:
        with open(f) as data_file:
            data = json.load(data_file)
            d = {}
            d['path'] = f
            d['data'] = data
            json_data.append(d)

    return json_data


def convert_html_to_txt(files):

    for f in files:
        html = open(f)
        soup = BeautifulSoup(html)
        divs = soup.find_all('div')
        txt = ''
        for div in divs:
            if len(div.find_all('div')) == 0:
                txt += div.get_text().encode('utf-8') + "\n\n"
        head, tail = os.path.split(f)
        name = tail[:-5]
        with open('txt_from_html/' + name + '.txt', 'w+') as txt_file:
            txt_file.write(txt)
            txt_file.close()


    #return json_data


def save_json(data, path):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)

#files = ['/Users/vitaliyvrublevskiy/contracts_2010/01/04/1AXOw9oDa18zA7ZvTymzzi.html']
files = []
find_files(files, [path_to_dataset], ['.html'])
convert_html_to_txt(files)
#data = generate_combined_meta_data(files[:])
#save_json(data, 'short.json')

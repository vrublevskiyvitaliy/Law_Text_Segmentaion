import os
import json

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


def save_json(data, path):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)

files = []
find_files(files, [path_to_dataset], ['.json'])
data = generate_combined_meta_data(files[:300])
save_json(data, 'short.json')

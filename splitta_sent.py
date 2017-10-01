import os

path_to_dataset = 'txt_from_html'


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


files = []
find_files(files, [path_to_dataset], ['.txt'])
path_to_exec = 'splitta/sbd.py'

for f in files:
    head, tail = os.path.split(f)
    os.system('python ' + path_to_exec + ' -m model_nb -t ' + f + ' -o ' + 'segmented_by_splitta/' + tail)



import json
from random import shuffle


def write(file, data):
    f = open(file, 'w')
    for s in data:
        f.write(s['text'] + " __clusterTitleType__" + s['clusterTitleType'] + " \n")
    f.close()


def generate_test():
    with open('all_sections_filtered_cluster_80.json') as data_file:
        data = json.load(data_file)

    shuffle(data)
    train = int(len(data) * 0.6)
    write('train_80.txt', data[:train])
    write('test_80.txt', data[train:])



generate_test()
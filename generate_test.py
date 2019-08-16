import json


def statistic():
    with open('all_sections_filtered+cluster.json') as data_file:
        data = json.load(data_file)

    chars = 800 * 8

    all_count = len(data)
    percent = 0
    filtered = []
    for s in data:
        if len(s['text']) > chars:
            percent += 1
        else:
            filtered.append(s)

    with open('all_sections_filtered_cluster_90.json', 'w') as outfile:
       json.dump(filtered, outfile)
    print(1. * percent / all_count)

statistic()
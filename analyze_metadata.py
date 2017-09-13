__author__ = 'vitaliyvrublevskiy'

import json


json_path = '1.json'



def prepare_title(title):
    t = title.lower()
    trash = ['.', ',', '`', '(', ')', '[', ']', '-', ':']
    for char in trash:
        t = t.replace(char, '')

    for i in range(10):
        t = t.replace(str(i), '')

    return t


def generate_word_dictionary():
    with open(json_path) as data_file:
        data = json.load(data_file)
    titles = []
    for record in data:
        titles.append(record['data']['title'])

    word_dictionary = {}

    for title in titles:
        if title is None:
            continue
        title = prepare_title(title)
        words = title.split(' ')
        for word in words:
            if len(word) == 0:
                continue
            if word in word_dictionary:
                word_dictionary[word] += 1
            else:
                word_dictionary[word] = 1

    return word_dictionary

words = generate_word_dictionary()

sort_dict = sorted(words.iteritems(), key=lambda (k,v): (v,k), reverse=True)

y = 0




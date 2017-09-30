__author__ = 'vitaliyvrublevskiy'
from nltk.corpus import stopwords
import json


json_path = '1.json'
AMOUNT_OF_MOST_USED = 400


def prepare_title(title):
    t = title.lower()
    trash = ['.', ',', '`', '(', ')', '[', ']', '-', ':']
    for char in trash:
        t = t.replace(char, '')

    for i in range(10):
        t = t.replace(str(i), '')

    return t


def save_most_used_words(words):
    path = 'wost_used_words_in_title.json'
    with open(path, 'w') as data_file:
        json.dump(words, data_file)


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
words = {v: k for v, k in words.iteritems() if not v in stopwords.words("english")}

sort_dict = sorted(words.iteritems(), key=lambda (k, v): (v, k), reverse=True)

most_used = []
i = 0
for v, k in sort_dict:
    if i < AMOUNT_OF_MOST_USED:
        most_used.append(v)
    print (v, k)
    i += 1

save_most_used_words(most_used)




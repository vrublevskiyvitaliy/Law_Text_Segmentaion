import os
import json
from nltk.tokenize import sent_tokenize, word_tokenize

class StructuredText:

    def __init__(self, path):
        self.path = path
        self.set_id()
        self.path_to_metadata = '1.json'
        self.set_metainfo()
        with open(path) as f:
            self.content = f.readlines()
        self.structure_text = {}
        self.structure_text['paragraph'] = []
        self.filter_content()
        self.divide_by_paragrahp()
        self.divide_by_sent()
        self.generate_all_sent()
        self.generate_text_string()



    def set_id(self):
        head, tail = os.path.split(self.path)
        self.id = tail[:-4]


    def filter_line(self, line):
        ll = ''
        for l in line:
            if (ord(l)) < 128:
                ll += l
        to_replace = ["\n", "\r", "\t", " ", "	", "	"]
        for rep in to_replace:
            line = line.strip(rep)
        return ll

    def filter_content(self):
        self.content = [x.strip() for x in self.content]
        self.filtered_content = []
        for line in self.content:
            line = self.filter_line(line)
            if len(line) > 0:
                self.filtered_content.append(line)

    def divide_by_paragrahp(self):
        self.content = [x.strip() for x in self.content]
        paragraph = ''
        for line in self.content:
            line = self.filter_line(line)
            if len(line) > 0:
                paragraph += line + ' '
            elif len(paragraph) > 0:
                self.structure_text['paragraph'].append({
                    'content': paragraph,
                    'sent': []
                })
                paragraph = ''


    def divide_by_sent(self):
        for paragraph in self.structure_text['paragraph']:
            sent = sent_tokenize(paragraph['content'])
            paragraph['sent'] = sent

    def write_to_file(self, path):
        file = open(path, 'w')

        for paragraph in self.structure_text['paragraph']:
            file.write("**********************\n")
            for s in paragraph['sent']:
                file.write(s + "\n")

        file.close()

    def generate_all_sent(self):
        self.all_sent = []
        for paragraph in self.structure_text['paragraph']:
            for s in paragraph['sent']:
                self.all_sent.append(s)

    def generate_text_string(self):
        self.text_string = ''
        for s in self.filtered_content:
            self.text_string += s + "\n"

    def write_to_file_full_text_sentances(self, path):
        sent = sent_tokenize(self.text_string)
        file = open(path, 'w')
        for s in sent:
            file.write(s + "\n")
        file.close()

    def set_metainfo(self):
        with open(self.path_to_metadata) as data_file:
            data = json.load(data_file)
            data = data[:102]

        self.meta = None

        for record in data:
            if record['data']['id'] == self.id:
                self.meta = record
                break


    def find_title(self):
        possible_titles = self.all_sent[:10]
        with open('wost_used_words_in_title.json') as f:
            most_used_words = json.load(f)

        result = []
        for item in possible_titles:
            count = 0
            words = word_tokenize(item)
            for w in words:
                if w in most_used_words:
                    count += 1
            upper = sum(1 for c in item if c.isupper())
            result.append({
                'count': count,
                'percentage': 1. * count / len(words),
                'title': item,
                'upper': 1. * upper / len(item),
            })

        result = sorted(result, key=lambda v: v['upper'], reverse=True)
        return result

# coding=utf-8
from os import listdir
from os.path import isfile, join
from nltk.tokenize import sent_tokenize

txt_path = 'txt/'
txt_segmented_path = 'segmented/'


class StructuredText:

    def __init__(self, path):
        self.path = path
        with open(path) as f:
            self.content = f.readlines()
        self.structure_text = {}
        self.structure_text['paragraph'] = []
        self.filter_content()
        self.divide_by_paragrahp()
        self.divide_by_sent()
        self.generate_all_sent()

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
        for line in self.filtered_content:
            self.structure_text['paragraph'].append({
                'content': line,
                'sent': []
            })

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


def filter_txt():
    files_txt = [f for f in listdir(txt_path) if isfile(join(txt_path, f)) and f[-3:] == 'txt']

    for file in files_txt:
        txt_before_path = txt_path + file
        txt_filtered_path = txt_segmented_path + file
        text = StructuredText(txt_before_path)
        text.write_to_file(txt_filtered_path)

filter_txt()
# encoding=utf-8
import os
import docx2txt
import json
from nltk.tokenize import sent_tokenize, word_tokenize
from ListHelper import ListHelper
from segtok.segmenter import split_single





class StructuredText:

    def __init__(self, path):
        self.path = path
        self.from_html = False
        self.set_id()
        self.path_to_metadata = '1.json'
        self.set_metainfo()
        self.read_content()
        self.structure_text = {}
        self.structure_text['paragraph'] = []
        self.filter_content()
        self.divide_by_paragrahp()
        self.divide_by_sent()
        self.generate_all_sent()
        self.generate_text_string()
        self.sections = []
        print('Title: ' + self.find_title())

    def read_content(self):
        if self.path[-3:] == 'txt':
            self.read_txt()
        elif self.path[-4:] == 'docx' or self.path[-3:] == 'doc':
            self.read_docx()
        else:
            raise ValueError('Couldnt recognize file')

    def read_txt(self):
        with open(self.path) as f:
            self.content = f.readlines()

    def read_docx(self):
        self.from_html = False
        self.content = docx2txt.process(self.path).encode('utf-8')
        self.content = self.content.split("\n")

    def set_id(self):
        head, tail = os.path.split(self.path)
        self.id = tail[:-4]

    def filter_line(self, line):
        ll = ''
        # todo: fix this
        for l in line:
            if (ord(l)) < 128:
                ll += l
        to_replace = ["\n", "\r", "\t", " ", "	", "	", "_"] # should we add _ ?
        for rep in to_replace:
            ll = ll.strip(rep)
        return ll

    def filter_content(self):
        self.content = [x.strip() for x in self.content]
        self.filtered_content = []
        for line in self.content:
            line = self.filter_line(line)
            if len(line) > 0:
                self.filtered_content.append(line)

    def divide_by_paragrahp(self):
        # from html
        if True:
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
        else:
            # from docx converted to txt
            self.content = [x.strip() for x in self.content]
            for line in self.content:
                line = self.filter_line(line)
                if len(line) > 0:
                    self.structure_text['paragraph'].append({
                        'content': line,
                        'sent': []
                    })

    def divide_by_sent(self):
        for paragraph in self.structure_text['paragraph']:
            if False:
                # NLTK
                sent = sent_tokenize(paragraph['content'])
            else:
                # segtok
                sent = split_single(paragraph['content'])
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
        next_is_title = False
        for item in possible_titles:
            if len(item) == 0:
                continue
            count = 0
            words = word_tokenize(item)
            if next_is_title:
                next_is_title = False
                return item

            if 'Exhibit' in item:
                next_is_title = True
            for w in words:
                if w.lower() in most_used_words:
                    count += 1
            upper = sum(1 for c in item if c.isupper())
            result.append({
                'count': count,
                'percentage': 1. * count / len(words),
                'title': item,
                'upper': 1. * upper / len(item),
            })

        result = sorted(result, key=lambda v: v['upper'], reverse=True)
        return result[0]['title']

    def write_list_to_file(self, path):
        file = open(path, 'w')
        for s in self.grouped_list_sentances:
            file.write(s['sss'] + "\n")
        file.close()

    def find_lists(self):
        self.list_sentances = []
        for sentence in self.all_sent:
            prefix = ListHelper.get_possible_list_id(sentence)
            self.list_sentances.append({
                'sentence' : sentence,
                'prefix' : prefix,
                'type': ListHelper.get_prefix_type(prefix)
            })
        self.group_lists_structure()
        self.post_analyze_lists_structure()

    def group_lists_structure(self):
        list_stack = []
        stack_of_all_structure = [
            []
        ]
        for s in self.list_sentances:
            sentence = s['sentence']
            prefix = s['prefix']
            prefix_type = s['type']
            if len(prefix) == 0:
                stack_of_all_structure[-1].append({
                    'sentence': sentence,
                    'is_list_item': False,
                })
            else:
                if len(list_stack) > 0:
                    # if the same type
                    while len(list_stack) > 0:
                        last_element = list_stack[-1]
                        if ListHelper.is_prefixes_neighboring(last_element['prefix'], s['prefix']):
                            # continue the same level
                            list_stack.pop()
                            list_stack.append(s)
                            stack_of_all_structure[-1].append({
                                'sentence': sentence,
                                'is_list_item': True,
                                'is_list_beggining': False,
                                'prefix_type':  prefix_type,
                            })
                            break
                        else:
                            # start new list
                            if ListHelper.is_prefix_begin_list(s['prefix']):
                                list_stack.append(s)
                                stack_of_all_structure.append([{
                                    'sentence': sentence,
                                    'is_list_item': True,
                                    'is_list_beggining': True,
                                    'prefix_type':  prefix_type,
                                }])
                                break
                            else:
                                # close previous list
                                list_stack.pop()
                                last_list = stack_of_all_structure[-1]
                                stack_of_all_structure = stack_of_all_structure[:-1]
                                stack_of_all_structure[-1].append(last_list)


                else:
                    list_stack.append(s)
                    stack_of_all_structure.append([{
                        'sentence': sentence,
                        'is_list_item': True,
                        'is_list_beggining': True,
                        'prefix_type':  prefix_type,
                    }])

        while len(list_stack) > 0:
            list_stack.pop()
            last_list = stack_of_all_structure[-1]
            stack_of_all_structure = stack_of_all_structure[:-1]
            stack_of_all_structure[-1].append(last_list)

        assert len(stack_of_all_structure) == 1
        self.list_structure = stack_of_all_structure[0]

    def generate_html_content(self, elements):
        content = ''
        for element in elements:
            if type(element) is list:
                content += "<ul>"
                content += self.generate_html_content(element)
                content += "</ul>"
            else:
                if element['is_list_item']:
                    content += '<li>'
                    content += element['sentence']
                    content += '</li>'
                else:
                    content += element['sentence']
        return content

    def write_group_lists_structure(self, path):
        file = open(path, 'w')
        content = self.generate_html_content(self.list_structure)
        file.write(content)
        file.close()

    def analyze_list_structure(self):
        if len(self.list_structure) == 0:
            print 'No structure'
            return
        else:
            # we need to find a list at 0 level with biggest amount of words

            index_of_main_list = None
            max_chars = 0
            for index, element in enumerate(self.list_structure):
                if type(element) is list:
                    if index_of_main_list is None:
                        index_of_main_list = index
                        max_chars = self.count_chars(element)
                    else:
                        current_chars = self.count_chars(element)
                        if current_chars > max_chars:
                            max_chars = current_chars
                            index_of_main_list = index

            if index_of_main_list is None:
                print 'No main list'
                return
            # here we have our main list
            # we can find out name of section

            for index, element in enumerate(self.list_structure[index_of_main_list]):
                if type(element) is not list and element['is_list_item']:
                    element['SECTION_NAME'] = element['sentence']
                    self.sections.append(element['sentence'])

    def count_chars(self, elements):
        chars = 0
        for element in elements:
            if type(element) is list:
                chars += self.count_chars(element)
            else:
                chars += len(element['sentence'])

        return chars

    # remove inner list from outer
    # todo: fix numbers
    def post_analyze_lists_structure(self):
        for index, element in enumerate(self.list_structure):
            if type(element) is list:
                if type(element[-1]) is list:
                    # check coef
                    outer_list_size = self.count_chars(element)
                    inner_list_size = self.count_chars(element[-1])
                    if (inner_list_size * 1.) / outer_list_size > 0.8:
                        # need to move it out
                        last_list = element[-1]
                        self.list_structure[index] = self.list_structure[index][:-1]
                        self.list_structure.insert(index + 1, last_list)
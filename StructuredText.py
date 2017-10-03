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

    def write_list_to_file(self, path):
        file = open(path, 'w')
        for s in self.grouped_list_sentances:
            file.write(s['sss'] + "\n")
        file.close()

    def find_lists(self):
        self.list_sentances = []
        for s in self.all_sent:
            prefix = self.get_possible_list_id(s)
            prefix_type = None
            if len(prefix) > 0:
                ss = s[len(prefix):]
                prefix_type = self.get_prefix_type(prefix)
                ss = '<LIST_ITEM type=' + prefix_type + '>' + prefix + '</LIST_ITEM>' + ss
            else:
                ss = s
            self.list_sentances.append({
                's' : s,
                'ss' : ss,
                'prefix' : prefix,
                'prefix_type' : prefix_type,
            })
        self.group_lists()

    def group_lists(self):
        # <ol>
        # <li> </li>
        start_list = {
            'sss': '<ul>'
        }
        end_list = {
            'sss': '</ul>'
        }

        stack = []
        self.grouped_list_sentances = []
        flag_found_list = False
        for s in self.list_sentances:
            s['sss'] = s['s']
            if len(s['prefix']) == 0:
                self.grouped_list_sentances.append(s)
            else:
                flag_found_list = True
                s['sss'] = '<li>' + s['s'] + '</li>'

                if len(stack) > 0:
                    # if the same type
                    while len(stack) > 0:
                        last_element = stack[-1]
                        if self.is_prefixes_neighboring(last_element['prefix'], s['prefix']):
                            stack.pop()
                            stack.append(s)
                            break
                        else:
                            # start new list
                            if self.is_prefix_begin_list(s['prefix']):
                                self.grouped_list_sentances.append(start_list)
                                stack.append(s)
                                break
                            else:
                                # close previous list
                                self.grouped_list_sentances.append(end_list)
                                stack.pop()
                else:
                    self.grouped_list_sentances.append(start_list)
                    stack.append(s)

                self.grouped_list_sentances.append(s)
        while len(stack) > 0:
            self.grouped_list_sentances.append(end_list)
            stack.pop()


    def get_prefix_type(self, prefix):
        if prefix == '(i)' or prefix == '(v)':
            return 'roman_()'
        prefixes = self.get_list_begginng_by_type()
        for key, value in prefixes.iteritems():
            if prefix in value:
                return key

        # then just number
        prefix = prefix[:]
        prefix = prefix.strip('.')
        dots = sum(1 for c in prefix if c == '.')
        return 'number' + str(dots)

    def is_prefix_begin_list(self, prefix):
        prefixes = self.get_list_begginng_by_type()
        prefix_type = self.get_prefix_type(prefix)
        if prefix_type in prefixes:
            return prefixes[prefix_type][0] == prefix
        else:
            # number
            prefix = prefix.strip('.')
            dots = sum(1 for c in prefix if c == '.')
            if dots > 0:
                prefix = prefix.split('.')[-1]
            return int(prefix) == 1

    def is_prefixes_neighboring(self, first_prefix, second_prefix):
        first_type = self.get_prefix_type(first_prefix)
        second_type = self.get_prefix_type(second_prefix)
        if self.get_prefix_type(first_prefix) != self.get_prefix_type(second_prefix):
            return False
        else:
            # todo: check if they are near, like 1 2 5 ?
            return True

    def get_possible_list_id(self, sentance):
        prefixes = self.get_list_begginng_by_type()

        for key, value in prefixes.iteritems():
            for prefix in value:
                if sentance.startswith(prefix):
                    return prefix

        possible_id = ''
        for char in sentance:
            if not char.isalpha() or char == '.':
                possible_id += char
            else:
                break

        return possible_id

    def get_list_begginng_by_type(self):
        types = dict()
        # low letter
        prefixes = []
        for i in range(ord('a'), ord('z')):
            prefixes.append(chr(i) + '.')
        types['low_letter'] = prefixes

        prefixes = []
        for i in range(ord('A'), ord('Z')):
            prefixes.append('(' + chr(i) + ')')
        types['big_letter_()'] = prefixes
        prefixes = ['(i)', '(ii)', '(iii)', '(iv)', '(v)', '(vi)', '(vii)', '(viii)']
        types['roman_()'] = prefixes
        prefixes = []
        for i in range(ord('a'), ord('z')):
            prefixes.append('(' + chr(i) + ')')
        types['low_letter_()'] = prefixes
        return types

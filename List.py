# encoding=utf-8
import re
INT_MAX = 100


class ListItem:
    def __init__(self, sentence):
        self.sentence = sentence
        self.prefixes = []
        self.prefix = ''
        self.init_prefixes()
        self.list_name = ''
        self.regex = ''

    def is_in_prefixes(self):
        starts_with_prefix = False
        if self.sentence is None:
            return starts_with_prefix
        try:
            if re.match('^' + self.regex, self.sentence):
                starts_with_prefix = True
                self.prefix = re.search(self.regex, self.sentence).group(0)
        except TypeError as e:
            print e.message
            print self.regex
            print self.sentence
            print 'is_in_prefixes'

        return starts_with_prefix

    def is_list_item(self):
        return self.is_in_prefixes()

    def init_prefixes(self):
        pass

    def is_begining_list(self):
        return len(self.prefixes) > 1 and self.prefixes[0] == self.prefix

    def get_next_prefix(self, prefix):
        try:
            index = self.prefixes.index(prefix) + 1
            next_prefix = self.prefixes[index]
        except ValueError as e:
            next_prefix = None
        except IndexError as e:
            print e.message
            print prefix
            print "Get next prefix"
            next_prefix = None
        return next_prefix


class LowLetterList(ListItem):
    """

    Something like a. b. c.

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'low_letter'
        self.regex = '[a-z]\.'

    def init_prefixes(self):
        for i in range(ord('a'), ord('z') + 1):
            self.prefixes.append(chr(i) + '.')


class NumberOneLevelList(ListItem):
    """

    Something like 1. 2. 3.

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'number0'
        self.regex = '[1-9]\\d*\.'

    def init_prefixes(self):
        pass
        #for i in range(1, INT_MAX):
        #    self.prefixes.append(str(i) + '.')

    def is_neighboring(self, first_prefix, second_prefix):
        if re.match('^' + self.regex + '$', first_prefix) and re.match('^' + self.regex + '$', second_prefix):
            first = first_prefix.split('.')[0]
            second = second_prefix.split('.')[0]
            return int(first) + 1 == int(second)
        else:
            return False

    def get_next_prefix(self, prefix):
        parts = prefix.split('.')
        parts[0] = str(int(parts[0]) + 1)
        return str(parts[0]) + '.'

    def is_begining_list(self):
        p = self.sentence.strip('.')

        return int(p) == 1


class NumberTwoLevelList(ListItem):
    """

    Something like 1.1 1.2 2.3

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'number1'
        self.regex = '[1-9]\\d*\.\\d+'

    def init_prefixes(self):
        pass
        #for i in range(1, INT_MAX):
        #    for j in range(1, INT_MAX):
        #        self.prefixes.append(str(i) + '.' + str(j))

    def is_begining_list(self):
        second_part_prefix = self.prefix.split('.')[1]
        return int(second_part_prefix) == 1

    def get_next_prefix(self, prefix):
        parts = prefix.split('.')
        parts[1] = str(int(parts[1]) + 1)
        return '.'.join(parts)

    def is_neighboring(self, first_prefix, second_prefix):
        if re.match('^' + self.regex + '$', first_prefix) and re.match('^' + self.regex + '$', second_prefix):
            first = first_prefix.split('.')[1]
            second = second_prefix.split('.')[1]
            return int(first) + 1 == int(second)
        else:
            return False


class NumberThreeLevelList(ListItem):
    """

    Something like 1.1.1 1.2.1 2.3.1

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'number2'
        self.regex = '[1-9]\\d*\.\\d+\.\\d+'

    def init_prefixes(self):
        pass
        # for i in range(1, INT_MAX):
        #     for j in range(1, INT_MAX):
        #         for y in range(1, 20):
        #             self.prefixes.append(str(i) + '.' + str(j) + '.' + str(y))

    def is_begining_list(self):
        second_part_prefix = self.prefix.split('.')[2]
        return int(second_part_prefix) == 1

    def get_next_prefix(self, prefix):
        parts = prefix.split('.')
        parts[2] = str(int(parts[2]) + 1)
        return '.'.join(parts)

    def is_neighboring(self, first_prefix, second_prefix):
        if re.match('^' + self.regex + '$', first_prefix) and re.match('^' + self.regex + '$', second_prefix):
            first = first_prefix.split('.')[2]
            second = second_prefix.split('.')[2]
            return int(first) + 1 == int(second)
        else:
            return False

class BigLetterBracketList(ListItem):
    """

    Something like (A) (B) (C)

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'big_letter_()'
        self.regex = '\([A-Z]\)'

    def init_prefixes(self):
        for i in range(ord('A'), ord('Z') + 1):
            self.prefixes.append('(' + chr(i) + ')')


class RomanBracketList(ListItem):
    """

    Something like (i) (ii) (iii)

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'roman_()'

    def init_prefixes(self):
        self.prefixes = ['(i)', '(ii)', '(iii)', '(iv)', '(v)', '(vi)', '(vii)', '(viii)']

    def is_in_prefixes(self):
        starts_with_prefix = False
        if self.sentence is None:
            return starts_with_prefix

        for prefix in self.prefixes:
            if self.sentence.startswith(prefix):
                starts_with_prefix = True
                self.prefix = prefix
                break

        return starts_with_prefix

class RomanDotList(ListItem):
    """

    Something like i. ii. iii.

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'roman_dot'

    def init_prefixes(self):
        self.prefixes = ['i.', 'ii.', 'iii.', 'iv.', 'v.', 'vi.', 'vii.', 'viii.']

    def is_in_prefixes(self):
        starts_with_prefix = False
        if self.sentence is None:
            return starts_with_prefix

        for prefix in self.prefixes:
            if self.sentence.startswith(prefix):
                starts_with_prefix = True
                self.prefix = prefix
                break

        return starts_with_prefix


class LowLetterBracketList(ListItem):
    """

    Something like (a) (b) (c)

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'low_letter_()'
        self.regex = '\([a-z]\)'

    def init_prefixes(self):
        for i in range(ord('a'), ord('z') + 1):
            self.prefixes.append('(' + chr(i) + ')')


class NumberBracketList(ListItem):
    """

    Something like 1) 2) 3)

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'number_)'
        self.regex = '\\d+\)'

    def init_prefixes(self):
        for i in range(1, INT_MAX):
            self.prefixes.append(str(i) + ')')


class CharBracketList(ListItem):
    """

    Something like a) b) c)

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'char_)'
        self.regex = '\\w\)'

    def init_prefixes(self):
        for i in range(ord('a'), ord('z') + 1):
            self.prefixes.append(chr(i) + ')')


class BigCharDotList(ListItem):
    """

    Something like A. B. C.

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'big_char_.'
        self.regex = '[A-Z]\.'

    def init_prefixes(self):
        for i in range(ord('A'), ord('Z') + 1):
            self.prefixes.append(chr(i) + '.')


class ArticleNumberDotList(ListItem):
    """

    Something like ARTICLE 1. ARTICLE 2.

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'article_number_.'
        self.regex = 'ARTICLE\ \\d+\.'

    def init_prefixes(self):
        for i in range(1, INT_MAX):
            self.prefixes.append('ARTICLE ' + str(i) + '.')


class SectionNumberDotList(ListItem):
    """

    Something like Section 1. Section 2.

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'section_number_.'
        self.regex = 'Section\ \\d+\.'

    def init_prefixes(self):
        for i in range(1, INT_MAX):
            self.prefixes.append('Section ' + str(i) + '.')


class SectionCapsNumberDotList(ListItem):
    """

    Something like SECTION 1. SECTION 2.

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'section_caps_number_.'
        self.regex = 'SECTION\ \\d+\.'

    def init_prefixes(self):
        for i in range(1, INT_MAX):
            self.prefixes.append('SECTION ' + str(i) + '.')


class SectionBracketsWithoutOrderList(ListItem):
    """

    Something like (A) (B) (X)

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'big_letter_()'
        self.regex = '\([A-Z]\)'

    def init_prefixes(self):
        for i in range(ord('A'), ord('Z') + 1):
            self.prefixes.append('(' + chr(i) + ')')

    def is_neighboring(self, first_prefix, second_prefix):
        if re.match('^' + self.regex + '$', first_prefix) and re.match('^' + self.regex + '$', second_prefix):
            return True
        else:
            return False

    def is_begining_list(self):
        p = self.sentence.strip('.')
        return self.sentence.strip('(').strip(')') == 'A'

# ADD ARTICLE I , II, 1E7XxSctOZ1kmCL3gRr3Sq
# Chapter ONE, TWO, .. 1e9lEXRT6nr59q4kb8LulD
# encoding=utf-8


class ListItem:
    def __init__(self, sentence):
        self.sentence = sentence
        self.prefixes = []
        self.prefix = ''
        self.init_prefixes()
        self.list_name = ''

    def is_list_item(self):
        return False

    def is_in_prefixes(self):
        starts_with_prefix = False

        for prefix in self.prefixes:
            if self.sentence.startswith(prefix):
                starts_with_prefix = True
                self.prefix = prefix
                break

        return starts_with_prefix

    def is_list_item(self):
        return self.is_in_prefixes()

    def init_prefixes(self):
        pass

    def is_begining_list(self):
        return len(self.prefixes) > 1 and self.prefixes[0] == self.prefix


class LowLetterList(ListItem):
    """

    Something like a. b. c.

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'low_letter'

    def init_prefixes(self):
        for i in range(ord('a'), ord('z')):
            self.prefixes.append(chr(i) + '.')


class NumberOneLevelList(ListItem):
    """

    Something like 1. 2. 3.

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'number0'

    def init_prefixes(self):
        for i in range(1, 40):
            self.prefixes.append(str(i) + '.')


class NumberTwoLevelList(ListItem):
    """

    Something like 1.1 1.2 2.3

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'number1'

    def init_prefixes(self):
        for i in range(1, 40):
            for j in range(1, 40):
                self.prefixes.append(str(i) + '.' + str(j))

    def is_begining_list(self):
        second_part_prefix = self.prefix.split('.')[1]
        return second_part_prefix == '1'


class BigLetterBracketList(ListItem):
    """

    Something like (A) (B) (C)

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'big_letter_()'

    def init_prefixes(self):
        for i in range(ord('A'), ord('Z')):
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


class LowLetterBracketList(ListItem):
    """

    Something like (a) (b) (c)

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'low_letter_()'

    def init_prefixes(self):
        for i in range(ord('a'), ord('z')):
            self.prefixes.append('(' + chr(i) + ')')


class NumberBracketList(ListItem):
    """

    Something like 1) 2) 3)

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'number_)'

    def init_prefixes(self):
        for i in range(1, 40):
            self.prefixes.append(str(i) + ')')


class CharBracketList(ListItem):
    """

    Something like a) b) c)

    """
    def __init__(self, sentence):
        ListItem.__init__(self, sentence)
        self.list_name = 'char_)'

    def init_prefixes(self):
        for i in range(ord('a'), ord('z')):
            self.prefixes.append(chr(i) + ')')


list_classes = {
    'LowLetterList': LowLetterList,
    'NumberTwoLevelList': NumberTwoLevelList,
    'NumberOneLevelList': NumberOneLevelList,
    'BigLetterBracketList': BigLetterBracketList,
    'RomanBracketList': RomanBracketList,
    'LowLetterBracketList': LowLetterBracketList,
    'NumberBracketList': NumberBracketList,
    'CharBracketList': CharBracketList,
}
# encoding=utf-8
from List import *


class ListHelper:
    @staticmethod
    def get_list_classes():
        return {
            'LowLetterList': LowLetterList,
            'NumberTwoLevelList': NumberTwoLevelList,
            'NumberOneLevelList': NumberOneLevelList,
            'BigLetterBracketList': BigLetterBracketList,
            'RomanBracketList': RomanBracketList,
            'LowLetterBracketList': LowLetterBracketList,
            'NumberBracketList': NumberBracketList,
            'CharBracketList': CharBracketList,
            'BigCharDotList': BigCharDotList,
            'ArticleNumberDotList': ArticleNumberDotList,
        }

    @staticmethod
    def get_prefix_type(prefix):
        types = []
        list_classes = ListHelper.get_list_classes()
        for list_class in list_classes:
            instance = list_classes[list_class](prefix)
            if instance.is_in_prefixes():
                types.append(instance.list_name)

        return types

    @staticmethod
    def get_next_prefix_for_type(prefix, type):
        list_classes = ListHelper.get_list_classes()
        for list_class in list_classes:
            instance = list_classes[list_class](prefix)
            if instance.is_in_prefixes() and instance.list_name == type:
                return instance.get_next_prefix(prefix)
        return None

    @staticmethod
    def get_possible_list_id(sentence):
        prefix = ''
        list_classes = ListHelper.get_list_classes()
        for list_class in list_classes:
            instance = list_classes[list_class](sentence)
            if instance.is_in_prefixes():
                prefix = instance.prefix if len(instance.prefix) > len(prefix) else prefix
        return prefix

    @staticmethod
    def is_prefix_begin_list(prefix):
        result = False
        list_classes = ListHelper.get_list_classes()
        for list_class in list_classes:
            instance = list_classes[list_class](prefix)
            if instance.is_in_prefixes() and instance.is_begining_list():
                result = True
        return result

    @staticmethod
    def is_prefixes_neighboring(first_prefix, second_prefix):
        first_type = ListHelper.get_prefix_type(first_prefix)
        second_type = ListHelper.get_prefix_type(second_prefix)
        if len(set(first_type).intersection(second_type)) == 0:
            return False
        else:
            for type in first_type:
                next_prefix = ListHelper.get_next_prefix_for_type(first_prefix, type)
                if next_prefix == second_prefix:
                    return True
                if ListHelper.is_prefixes_neighboring_inner(first_prefix, second_prefix, type):
                    return True
            return False

    @staticmethod
    def is_prefixes_neighboring_inner(first_prefix, second_prefix, type):
        list_classes = ListHelper.get_list_classes()
        for list_class in list_classes:
            instance = list_classes[list_class](first_prefix)
            if instance.list_name == type and hasattr(instance, 'is_neighboring'):
                return instance.is_neighboring(first_prefix, second_prefix)

        return False



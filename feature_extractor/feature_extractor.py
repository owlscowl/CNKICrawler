#! usr/bin/python
# coding=utf-8
import sys

import jieba
import jieba.analyse
import jieba.posseg as pseg
import multiprocessing

import mongo_utils.mongo_utils as mongo_utils
import collection_utils.collection_utils as collection_utils

reload(sys)
sys.setdefaultencoding('utf-8')

__author__ = 'roliy'

# jieba example
def jieba_example():
    raw = "我爱北京天安门"
    raw_seq = jieba.cut(raw)
    raw_seq_list = jieba.lcut(raw)
    raw_keyword = jieba.analyse.extract_tags(raw, topK=3, withWeight=False, allowPOS=())
    raw_with_ictclas = pseg.cut(raw)
    for word, flag in raw_with_ictclas:
        print(word, flag)


def cut_with_flag(raw_str, filter_invalid_word_flag=True):
    """

    :param raw_str: str
    :return: list[(str, str)]
    """
    res = [(a, b) for a, b in pseg.lcut(raw_str)]

    if filter_invalid_word_flag:
        return filter_invalid_word(res)
    else:
        return res


def build_tf(raw_str):
    """

    :param raw_str: str
    :return: list[(str, int)]
    """
    raw_seq_with_flag = cut_with_flag(raw_str)
    word_frequency_map = collection_utils.count_by(raw_seq_with_flag, lambda x: str(x[0]) + "-" + str(x[1]))
    res = []
    for key in word_frequency_map.keys():
        res.append((key, word_frequency_map[key]))
    return res


def parse_item(item):
    """

    :param item: dictionary
    :return: void
    """
    def add_abstract_seq(t):
        t['abstract_seq'] = build_tf(t['abstract'])

    def add_school_seq(t):
        t['school_seq'] = jieba.lcut_for_search(t['school'])

    def add_title_seq(t):
        t['title_seq'] = cut_with_flag(t['title'])

    add_abstract_seq(item)
    add_school_seq(item)
    add_title_seq(item)
    item['_id'] = str(item['_id'])

    return item


def filter_invalid_word(items):
    """

    :param items: list[(str, str)]
    :return:
    """
    def filter_char(t):
        return collection_utils.select(t, lambda x: u'x' not in x[1])

    def filter_stop_word(t):
        return collection_utils.select(t, lambda x: u'u' not in x[1])

    return filter_stop_word(filter_char(items))


def cursor_to_list(cursor):
    return [i for i in cursor]


def multiprocessing_groups(items, process_num, do_func, step):
    def start_process():
        print("starting %s\n" % multiprocessing.current_process().name)

    groups = [items[i:i + step] for i in range(0, len(items), step)]
    pool = multiprocessing.Pool(processes=process_num, initializer=start_process)
    res = pool.map(do_func, groups)
    pool.close()
    pool.join()
    return res


def parse_items_and_insert(array):
    data = [parse_item(i) for i in array]
    mongo_utils.insert_seq_paper_detail(data)


def parse_all():
    cursor = mongo_utils.get_all_paper_detail()
    result = cursor_to_list(cursor)
    multiprocessing_groups(result, 36, parse_items_and_insert, 250)


def main(argv):
    return


if __name__ == '__main__':
    main(sys.argv[1:])
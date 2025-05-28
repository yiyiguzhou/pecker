# coding=utf-8
import datetime
from project.script.testsuite.TestsuiteNormal import *
from project.lib.interface_test.utils import Singleton

# checkSort(data, sort_keyword, data_order) 判断排序，用于排序部分的验证
# parameter: data,类型：[{},{},{}]，对应返回值查到的返回值data中的列表;
#            sort_keyword,排序字段，类型：unicode或者int，unicode对应时间格式，int是数值型的判断，
#            data_order，升序降序，desc 或 asc
def check_sort(data, sort_keyword, data_order):
    i = 1
    result = True
    obj = Singleton.Singleton.get_instance("11", "22", False)
    while (result):
        if i < len(data):
            sort_word = data[i][sort_keyword]
            data_orders = ["DESC", "ASC"]
            expect_true(check_contain(data_order, data_orders), obj.id + " DESC/ASC输入校验")
            cmp_data(data_order, sort_word, data, i, sort_keyword)

            i = i + 1
        else:
            result = False

def cmp_data(data_order, sort_word, data, i, sort_keyword):
    obj = Singleton.Singleton.get_instance("11", "22", False)
    expect_true(check_contain(type(sort_word), [int, str]), obj.id + " 添加新种类")
    if isinstance(sort_word, int):
        if data_order == 'desc':
            expect_true(compare_size(int(data[i - 1][sort_keyword]), int(data[i][sort_keyword])), obj.id + " 排序错误")
        elif data_order == 'asc':
            expect_true(compare_size(int(data[i][sort_keyword]), int(data[i - 1][sort_keyword])), obj.id + " 排序错误")
    elif isinstance(sort_word, str):
        au_result = True
        for sa in sort_word:
            if not sa >= u'\u0030' and sa <= u'\u0039':
                au_result = False
                break

        if au_result:
            if data_order == 'desc':
                expect_true(compare_size(int(data[i - 1][sort_keyword]), int(data[i][sort_keyword])), obj.id + " 排序错误")
            elif data_order == 'asc':
                expect_true(compare_size(int(data[i][sort_keyword]), int(data[i - 1][sort_keyword])), obj.id + " 排序错误")
        else:
            s1 = data[i - 1][sort_keyword]
            s2 = data[i][sort_keyword]
            s1 = s1[:10] + " " + s1[10:]
            s2 = s2[:10] + " " + s2[10:]
            d1 = datetime.datetime.strptime(s1, '%Y-%m-%d %H:%M:%S')
            d2 = datetime.datetime.strptime(s2, '%Y-%m-%d %H:%M:%S')
            delta = d1 - d2
            d = delta.days
            if data_order == 'desc':
                expect_true(compare_size(0, d), obj.id + " 排序错误")
            elif data_order == 'asc':
                expect_true(compare_size(d, 0), obj.id + " 排序错误")

# find_list(d, rl) 找到返回值的列表，用于排序部分的验证
# parameter: data,类型：list或dict，对应返回值data;
#           rl,类型：list，空列表，用于存储找到的结果
def find_list(data, rl):
    if isinstance(data, list):
        rl.append(data)
    elif isinstance(data, dict):
        for k in data.keys():
            find_list(data[k], rl)
    return rl


def compare_size(a, b):
    if a>b or a == b:
        return True
    else:
        return False


def check_contain(s, total_list):
    if s in total_list:
        return True
    else:
        return False
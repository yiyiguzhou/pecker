import copy
import re
from project.script.testsuite.TestsuiteNormal import *
from project.lib.interface_test.database import DtbaseTable, Database
from project.lib.interface_test.testcase import cmpMethod, sort
from project.lib.interface_test.utils import generateReport, Singleton


def cmp_single_test_case6(single_test_case, data):
    # 排序判断原理：如果返回值里有排序的字段，调用check_sort函数根据传入的升序和降序进行排序判断，
    #            如果不在返回值里，去查询在不在已设置的SQL特殊查询中
    #            check_sort 无返回，若有错直接报错，已设置的SQL特殊查询返回list，与查到的id_list相比较
    sort_part, regular_part, exist_part, other_part = generateReport.get_all_special_parts(single_test_case)
    #special = generateReport.get_special_part_dict(data_all, "exist")
    #cmpMethod.check_regular_part(regular_part, data)
    if sort_part not in (None, {}, ""):
        single_test_case_check_sort(sort_part, data,single_test_case)

    if exist_part not in (None, {}, ""):
        cmpMethod.check_if_key_is_exist(data, exist_part)

    if regular_part not in (None, {}, ""):
        cmpMethod.check_regular_part(regular_part, data)


    single_test_case["expect_data_all"] = other_part
    if single_test_case["expect_data_all"] != {}:
        check_key_in_all_results(single_test_case, data)


def check_data(results, single_test_case):
    data = results
    if "expect_data_part" in single_test_case.keys():
        if single_test_case["expect_data_part"] != "":
            cmp_single_test_case5(single_test_case, data)
    if "expect_data_all" in single_test_case.keys():
        if single_test_case["expect_data_all"] != "":
            cmp_single_test_case6(single_test_case, data)


def single_test_case_check_sort(s, data, single_test_case):
    sort_keyword, data_order, temp_else = str(s).replace(" ","").split('||')
    check, sort_keyword = sort_keyword.split(":")
    print(sort_keyword, data_order)
    tl = sort.find_list(data, [])
    if sort_keyword in tl[0][0]:
        sort.check_sort(tl[0], sort_keyword, data_order.upper())
    else:
        check_sort_in_database(single_test_case, sort_keyword, tl)


def check_key_in_all_results(single_test_case, data):
    expect2 = eval(str(single_test_case["expect_data_all"]))
    places = [m.start() for m in re.finditer('/', single_test_case["url_place"])]
    place = places[len(places) - 2]
    file_name = str(single_test_case["url_place"])[place + 1:-1].replace('/', '_')
    # 复制一个空的expect21，用来存返回值
    expect21 = copy.deepcopy(expect2)
    expect21 = cmpMethod.change_expect(expect21)
    # 用空的集合存储返回值
    rlist = cmpMethod.get_result(expect21, data)
    # 与expect比较
    parameter = single_test_case["url_parameter"]
    cmpMethod.cmp_data2(expect2, rlist, file_name, parameter, "all")
    print('第二种比较成功')


def check_sort_in_database(single_test_case, sort_keyword, tl):
    trcf = DtbaseTable.Config_read()
    places = [m.start() for m in re.finditer('/', single_test_case["url_place"])]
    place = places[len(places) - 2]
    file_name = str(single_test_case["url_place"])[place + 1:-1].replace('/', '_')
    tresult = trcf.check_key_in_union(file_name, sort_keyword)
    if tresult == True:
        sql = trcf.generate_sql(file_name, sort_keyword, single_test_case["url_parameter"], "check_sort")
        check_result_sort(tl, file_name, sql)

    else:
        expect_true(trcf.check_special(file_name, sort_keyword), single_test_case['testcase_id'] + "排序部分：添加新的SQL语句")
        skey = file_name + "_" + sort_keyword
        sql = trcf.get_special_select(skey)[1].replace('\\', '').replace("\'", '')
        check_result_sort(tl, file_name, sql)

"""
def check_sort_in_database(single_test_case, sort_keyword, tl):
    trcf = DtbaseTable.Config_read()
    places = [m.start() for m in re.finditer('/', single_test_case["url_place"])]
    place = places[len(places) - 2]
    file_name = str(single_test_case["url_place"])[place + 1:-1].replace('/', '_')
    tresult = trcf.check_key_in_union(file_name, sort_keyword)
    if tresult == True:
        sql = trcf.generate_sql(file_name, sort_keyword, single_test_case["url_parameter"], "check_sort")
        check_result_sort(tl, file_name, sql)

    else:
        expect_true(trcf.check_special(file_name, sort_keyword), single_test_case['testcase_id'] + "排序部分：添加新的SQL语句")
        skey = file_name + "_" + sort_keyword
        sql = trcf.get_special_select(skey)[1].replace('\\', '').replace("\'", '')
        check_result_sort(tl, file_name, sql)
"""

def cmp_single_test_case5(single_test_case, data):
    expect1 = eval(str(single_test_case["expect_data_part"]))
    result = cmpMethod.cmp_data1(expect1, data)
    print('部分比較', result)
    expect_true(cmpMethod.cmp_data1(expect1, data), single_test_case['testcase_id'] + " 部分比较")


def get_host_and_database(file_name):
    trcf = DtbaseTable.Config_read()
    host = trcf.get_value(file_name)[0]
    if host == "":
        host = 'bd.gameplat2qc.w.qiyi.db'
    database = trcf.get_value(file_name)[1]
    return host, database


def check_result_sort(tl, file_name, sql):
    d = Database.Database()
    id_list = get_id_list(tl)
    host, database = get_host_and_database(file_name)

    get_list_result = d.get_list(sql, host, database)
    obj = Singleton.Singleton.get_instance("11", "22", False)
    for n in range(len(get_list_result)):
        expect_true(check_equal(str(get_list_result[n]),str(id_list[n])), obj.id + " 排序错误")
    return True


def get_id_list(tl):
    fid_list = []
    for i in tl[0]:
        if 'id' in i:
            fid_list.append(str(i['id']))
        elif 'game_id' in i:
            fid_list.append(str(i['game_id']))
    id_list = []
    for id in fid_list:
        if id not in id_list:
            id_list.append(id)
    return id_list


def check_equal(a,b):
    if a == b:
        return True
    else:
        return False
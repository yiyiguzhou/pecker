#coding=utf-8
import copy
import re
from project.lib.interface_test.database import DtbaseTable, Database
from project.lib.interface_test.testcase import runWay
from project.script.testsuite.TestsuiteNormal import *
from project.lib.interface_test.utils import Singleton


# 两种比较方式：比较某一项内的值或者比较每一项共有的某个值
# 第1种比较方式：比较某一项内的值
# cmp_data1(expect, data) 比较某一项内的值，用于类似于查看返回值全不全部分的验证
# parameter: data,类型：dict 或 list,对应返回值查到的返回值data中的列表;
#            expect, 期望值，类型：dict或者list

def change_list_and_dict(expect, data):
    if isinstance(data, dict):
        for key in data:
            if key not in data:
                return False
            elif isinstance(expect[key], list) and isinstance(data[key], dict):
                for e in range(len(expect)):
                    e_dict = {}
                    e_dict[key] = expect[key][e]
                    expect[key] = e_dict
            if not cmp_data1(expect[key], data[key]):
                return False
        return True

    elif isinstance(data, list):
        if isinstance(expect, dict):
            expect = [expect]
        change_list_and_dict(expect, data)
    else:
        pass
        return expect, data



def cmp_data1(expect, data):
    if isinstance(data, list) and isinstance(expect, dict):
        expect = [expect]
    if isinstance(expect, dict):
        for key in expect:
            if key not in data:
                return False
            elif isinstance(expect[key], list) and isinstance(data[key], dict):
                for e in range(len(expect)):
                    e_dict = {}
                    e_dict[key] = expect[key][e]
                    expect[key] = e_dict
            if not cmp_data1(expect[key], data[key]):
                return False
        return True

    elif isinstance(expect, list):
        for e in expect:
            index = index_of(e, data)
            if index == -1:
                return False
        return True

    else:

        if type(data) == 'unicode':
            data = data.replace(' ', '')
        else:
            data = str(data).replace(' ', '')
        expect = str(expect)

        """
        if expect != data:
            print ('!!!!', data, expect)
        """
        return expect == data

# indexof(e, data) 配合cmp_data1(expect, data) 使用的方法，用于判断list中的数据

def index_of(e, data):

    for d in data:
        if cmp_data1(e, d):
            return 1
    return -1

# 第2种比较方式：比较每一项的某个值
# 比较方法，1）生成空的expect字典，每个value值都是set类型
#          2）在返回值中根据空的字典找到对应的值，填写到字典中，如果待查找值不在返回值中则返回待查找值应在的多个字典
#          3）将返回的查找过得值的字典与expect相比较

# 1. change_expect(expect)，生成空的expect字典，将expect中的每一项的值装换为空的set

def change_expect(expect):
    if isinstance(expect, dict):
        for ek in expect:
            if not isinstance(expect[ek], dict) and not isinstance(expect[ek], list):
                expect[ek] = set([])
            change_expect(expect[ek])
    elif isinstance(expect, list):
        for l in expect:
            change_expect(l)
    else:
        pass
    return expect

# 2. get_result(expect, data)，根据查到的值替换expect，得到data中的值

def get_result(expect, data):
    if isinstance(data, list) and isinstance(expect, dict):
        expect = [expect]
    if isinstance(expect, dict):
        for ek in expect:
            if ek in data:
                if type(ek) == int:
                    for dkey in data:
                        if type(dkey) == int:
                            get_result(expect[ek], data[dkey])
                else:
                    if not isinstance(expect[ek], dict) and not isinstance(expect[ek], list):
                        expect[ek].add(str(data[ek]))

                    get_result(expect[ek], data[ek])
            else:
                # 返回值data中没有这个key，则加个标识符 *_，方便后续取数据库查询
                if str(ek).startswith("*_"):
                    expect[ek].append(data)
                else:
                    nek = '*_' + str(ek)
                    expect[nek] = list(expect[ek])
                    """
                    if isinstance(data, list):
                        expect[nek] = data
                    else:
                        expect[nek].append(data)
                    """
                    expect[nek].append(data)
                    expect.pop(ek)
    elif isinstance(expect, list):
        for el in expect:
            for ed in data:
                get_result(el, ed)
    else:
        pass
    return expect

# 3. cmp_data2(expect, result, filename) 比较每一项的某个值，用于类似于查看返回值中的所有游戏类型是否为xx游戏
# parameter: result,第二步的返回值;
#            expect, 期望值，类型：dict或者list
#            filename, 文件名，如果查不到，要根据文件名去数据库里查。
# 数据库比较有两种方式：1，带着返回值的id去数据库里查这些id的属性符不符合预期
#                     2，查出符合条件的列表，与返回值相比较（用于排序等判断）
def cmp_data2(data, expect, filename, parameter, used_flag):
    if isinstance(expect, dict):
        # 对结果中的每一个key
        for r in expect.keys():
            ss = expect[r]
            if isinstance(expect[r], dict) and isinstance(data[r], list):
                temp_expect_r = []
                temp_expect_r.append(expect[r])
                expect[r] = temp_expect_r
            if r == "*_page":
                check_page_in_database(expect[r], expect, filename, parameter)
            else:
                # 如果结果的key不在期望值中（加了*_标识），为了数据库查询
                if not r in data:
                    #check_result_in_database(expect[r], filename, expect, parameter, data)
                    check_result_in_database(r, filename, expect, parameter, data)
                else:
                    cmp_data2(data[r], expect[r], filename, parameter, used_flag)
    elif isinstance(expect, list):
        for r in expect:
            for e in data:
                cmp_data2(e, r, filename, parameter, used_flag)
    else:
        check_result(data, expect, used_flag)

def check_result_in_database(r, filename, result, parameter, expect):
    trcf = DtbaseTable.Config_read()
    r2 = copy.deepcopy(r)
    r2 = str(r2)[2:]
    # 判断key在不在数据库中（不联表）
    c_result = trcf.checkKey(filename, r2)
    id_list, ikey = get_id_list_from_data(result, r)
    id_list_content = ""
    for i in id_list:
        id_list_content = id_list_content + str(i) + ','

    # 如果返回值中有id_list，一般就是验证id的属性
    if id_list_content != '':
        result, filename, parameter = verify_id_attributes(ikey, id_list_content, c_result, filename, r2, result, r,
                                                              parameter)
        cmp_data2(expect, result, filename, parameter, "all")
    # 返回中没有id，就不是范围类的查询，目前只有分类下数量
    else:
        check_classification_quantity(filename, r2, parameter, result, r)



def check_r_in_sets_or_not(sets, r):
    if str(r) in sets:
        return True
    else:
        return False


def check_fuzzy_result(m_key, r):
    m = re.search(m_key, r, re.IGNORECASE)
    m_result = bool(m)
    return m_result


def check_result(data, expect, used_flag):
    if used_flag == "all":
        mark, sets = get_expect_dictand_mark(data)
        obj = Singleton.Singleton.get_instance("11", "22", False)
        if mark == 'ordinary':
            for r in expect:
                for s in sets:
                    if s.startswith("!"):
                        expect_false(check_r_in_sets_or_not(sets, r), obj.id + " ‘非’查询全部比较字段 " + str(r))
                    else:
                        expect_true(check_r_in_sets_or_not(sets, r), obj.id + " 全部比较字段 " + str(r))
        elif mark == 'fuzzy':
            m_key = str(data)[1:len(str(data)) - 1]
            for r in expect:
                expect_true(check_fuzzy_result(m_key, r), obj.id + " 模糊查询比较字段")
    elif used_flag == "exist":
        expect_true(check_r_is_regular_expression(data, expect), "正则比较某字段")


def check_r_is_regular_expression(data, expect):
    string = r''+expect+''
    expect_list = re.compile(string).findall(data)
    if len(expect_list) == 0:
        return False
    else:
        return True


def get_expect_dictand_mark(expect):
    sets = set([])
    if str(expect).startswith('$:'):
        expect = str(expect)[2:]
        ks = expect.split(',')
        for k in ks:
            sets.add(str(k))
    else:
        sets.add(str(expect))
    if re.match(r'%(.*)%', str(expect)):
        mark = 'fuzzy'
    else:
        mark = 'ordinary'
    return mark, sets

def check_classification_quantity(filename, r2, parameter, result, r):
    trcf = DtbaseTable.Config_read()
    t_result = trcf.check_key_in_union(filename, r2)
    obj = Singleton.Singleton.get_instance("11", "22", False)
    if t_result == True:
        sql = trcf.generate_sql(filename, r2, parameter, "")
        d = Database.Database()
        host, database = get_host_and_database(filename)
        rdict = d.get_dict(sql, host, database)
        expect_true(cmp_data1(rdict, result[r]), obj.id + " 数据库联表查询比较字段")

    else:
        expect_true(trcf.check_special(filename, r2), obj.id + " 添加新SQL语句")
        k = filename + "_" + r2
        sql = trcf.get_special_select(k).replace('\'', '').replace('\\', '')
        d = Database.Database()
        host, database = get_host_and_database(filename)
        rdict = d.get_dict(sql, host, database)
        expect_true(cmp_data1(rdict, result[r]), obj.id + " 预置SQL比较字段")


def verify_id_attributes(ikey, id_list_content, c_result, filename, r2, result, r, parameter):
    trcf = DtbaseTable.Config_read()
    id_list_content = ikey + ' in (' + id_list_content[:-1] + ')'
    condition = id_list_content
    obj = Singleton.Singleton.get_instance("11", "22", False)
    # key在数据库中（不联表）
    if c_result == True:
        tablename = trcf.get_value(filename)[1] + '.' + trcf.get_value(filename)[2]
        d = Database.Database()
        host, database = get_host_and_database(filename)
        drset = d.select_one_key(host, database, r2, tablename, condition)
        result[r2] = drset
        result.pop(r)
    # key不在数据库中（不联表），需要联表查询
    else:
        t_result = trcf.check_key_in_union(filename, r2)
        if t_result == True:
            d = Database.Database()
            host, database = get_host_and_database(filename)
            sql = trcf.generate_sql(filename, r2, parameter, "")
            drset = d.special_select(host, database, sql, condition, "", filename)

            result[r2] = drset
            result.pop(r)
        else:
            expect_true(trcf.check_special(filename, r2), obj.id + " 添加新接口配置文件")
            mark = filename + "_" + r2
            sql = trcf.get_special_select(mark)[1]
            sql = sql.replace('\\', '').replace('\'', '')
            d = Database.Database()
            host, database = get_host_and_database(filename)
            drset = d.special_select(host, database, sql, condition, "", filename)
            result[r2] = drset
            result.pop(r)
    return result, filename, parameter


def check_if_is_equal(a, b):
    if a==b:
        return True
    else:
        return False


def check_page_in_database(r, result, filename, parameter):
    r2 = r[2:]
    trcf = DtbaseTable.Config_read()
    t_result = trcf.check_key_in_union(filename, r2)
    obj = Singleton.Singleton.get_instance("11", "22", False)
    if t_result == True:
        id_list, ikey = get_id_list_from_data(result, r)
        sql = trcf.generate_sql(filename, r2, parameter, "")
        d = Database.Database()
        host, database = get_host_and_database(filename)
        get_list_result = d.get_list(sql, host, database)
        for n in range(len(get_list_result)):
            expect_true(check_if_is_equal(str(get_list_result[n]), str(id_list[n])), obj.id + " 全部比较字段")


def get_host_and_database(filename):
    trcf = DtbaseTable.Config_read()
    host = trcf.get_value(filename)[0]
    if host == "":
        host = 'bd.gameplat2qc.w.qiyi.db'
    database = trcf.get_value(filename)[1]
    return host, database

def getid_list(resultr):
    fid_list = []
    ikey = ""
    for i in resultr:
        if 'id' in i:
            ikey = 'id'
            fid_list.append(str(i['id']))
        elif 'game_id' in i:
            ikey = 'game_id'
            fid_list.append(str(i['game_id']))
    id_list = []
    for id in fid_list:
        if id not in id_list:
            id_list.append(id)
    return id_list, ikey

def get_id_list_from_data(result, r):
    fid_list = []
    ikey = ""
    for i in result[r]:
        if 'id' in i:
            ikey = 'id'
            fid_list.append(str(i['id']))
        elif 'game_id' in i:
            ikey = 'game_id'
            fid_list.append(str(i['game_id']))
    id_list = []
    for id in fid_list:
        if id not in id_list:
            id_list.append(id)
    return id_list, ikey


global exist_line_count
exist_line_count = 0
def get_exist_part_line(expect_part_dict, line_list, line):
    global exist_line_count
    if isinstance(expect_part_dict, dict):
        for d in expect_part_dict.keys():

            if not exist_line_count == 0:
                if str(line).endswith("-"):
                    line = line[:-1]
                lines = line.split("-")
                lines.pop(-1)
                line = "-".join(lines)
                line = line + "-"
                exist_line_count -= 1
            line = line + str(d) + "-"

            get_exist_part_line(expect_part_dict[d], line_list, line)
    elif isinstance(expect_part_dict, list):
        for l in range(len(expect_part_dict)):
            if not l == 0:
                expect_part_dict.pop(-1)
            get_exist_part_line(expect_part_dict[l], line_list, line)
    else:
        line = line + str(expect_part_dict) + "-"
        if str(line).endswith("exist-"):
            line_list.append(line[:-1])
        exist_line_count += 1
    return line_list


def check_if_key_is_exist_by_step(data, steps, exist_i):
    if isinstance(data, dict):
        if steps[exist_i] in data.keys():
            exist_i += 1
            if exist_i < len(steps):
                return check_if_key_is_exist_by_step(data[steps[exist_i - 1]], steps, exist_i)
            else:
                pass
        else:
            print("怎么没有呢")
            return False
    elif isinstance(data, list):
        for l in data:
            return check_if_key_is_exist_by_step(l, steps, exist_i)
    else:
        pass
    return True

def   check_if_key_is_exist(data, exist_part):
    exist_line_list = get_exist_part_line(exist_part, [], "")
    #print(exist_line_list)
    for l in exist_line_list:
        steps = l.split("-")
        steps = steps[:-2]
        expect_true(check_if_key_is_exist_by_step(data, steps, 0), "校验是否存在")


def transfer_regular_to_real_dict(regular_part):
    if isinstance(regular_part, dict):
        for d in regular_part.keys():
            if "test_type" in regular_part[d]:
                regular_part[d] = regular_part[d]["#text"]
            else:
                transfer_regular_to_real_dict(regular_part[d])
    elif isinstance(regular_part, list):
        for l in regular_part:
            transfer_regular_to_real_dict(l)
    else:
        pass
    return regular_part



def check_regular_part(regular_part, data):
    regular_part = transfer_regular_to_real_dict(regular_part)
    #print(regular_part)
    cmp_data2(data, regular_part, "", "", "exist")
    #check_result(regular_part, data, "exist")

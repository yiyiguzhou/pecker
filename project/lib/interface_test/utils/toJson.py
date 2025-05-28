# coding=utf-8
import json
import copy
import re
from project.script.testsuite.TestsuiteNormal import *
from project.lib.interface_test.utils import Singleton
# is_json(myjson) 判断传入的字符串是否能转换成Json格式
# parameter:myjson,类型：字符串，待转变为Json的字符串
def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True


# json_string(r_key, response_decode1, response_decode) 将传入的字符串中不能转换为Json格式的部分替换掉
# parameter:r_key,类型：字符串，待更改部分的key;
#           response_decode1, response_decode,类型：字符串，两个参数的值是一样的，一个用来定位买一个用来替换
def json_string(r_key, response_decode1, response_decode):
    if r_key in response_decode1:
        k_place = response_decode1.find(r_key)
        v_place = response_decode1.find(':\"', k_place) + 2
        if response_decode1[v_place - 1] == '\"' and response_decode1[v_place] != '"':
            if response_decode1[v_place] == '{':
                v_end_place = response_decode1.find('}"', v_place)
            else:
                v_end_place1 = response_decode1.find('\",\"', v_place)
                v_end_place2 = response_decode1.find('"}', v_place)
                if v_end_place1 < 0:
                    if v_end_place2 < 0:
                        obj = Singleton.Singleton.get_instance("11", "22", False)
                        expect_true(compare_size(0, v_end_place2),  obj.id + " 截取的末尾字符串错误")
                    else:
                        v_end_place = v_end_place2
                elif v_end_place2 < 0:
                    v_end_place = v_end_place1
                else:
                    if v_end_place1 < v_end_place2:
                        v_end_place = v_end_place1
                    else:
                        v_end_place = v_end_place2
            reinnit = response_decode1[v_place:v_end_place]
            rereplace = response_decode1[v_place:v_end_place].replace('\"', '')
            response_decode = response_decode.replace(reinnit, rereplace)
        response_decode1 = response_decode1[v_place:len(response_decode1)]
        return json_string(r_key, response_decode1, response_decode)
    else:
        return response_decode


#转换成Json
def to_json_string(data):
    data = data.replace("\\", "").replace(" ", "")
    data = delete_quotes(data)
    left = [m.start() for m in re.finditer("{", data)]
    right = [m.start() for m in re.finditer("}", data)]
    str = to_json(data, left, right).replace(" ", "")
    return str


# 先找里层括号，从左向右遍历，遇到一个右括号，就以此为基准，向左向右逐步判断，把多余的括号一层一层去掉。然后，从上一个基准点，向右寻找下一个基准点，直至遇到字符串结束
def to_json(data, left, right):
    r = 0
    flagr = True
    while (flagr):
        if r < len(right):
            l = len(left) - 1
            flagl = True
            while (flagl):
                if l >= 0 and r >= 0:
                    if left[l] < right[r]:
                        cresult = check_extra(data, left, right, l, r)
                        if cresult != False:
                            data = cresult
                        else:
                            data = data[:right[r]] + " " + data[right[r] + 1:]
                            right.pop(r)
                        r = r - 1
                        flagl = False
                    l = l - 1
                else:
                    flagl = False
            r = r + 1
        else:
            flagr = False
    for e in range(len(left)):
        data = data[:left[e]] + " " + data[left[e] + 1:]
    return data


# 检查是不是多余的括号
def check_extra(data, left, right, l, r):
    if l >= 0 and r >= 0:
        temp = data[left[l]:right[r] + 1]
        if is_json(temp):
            left.pop(l)
            right.pop(r)
            return data
        else:
            data = data[:left[l]] + " " + data[left[l] + 1:]

            l = l - 1
            return check_extra(data, left, right, l, r)
    else:
        return False


# 用来去除一个字典里多余的括号
def delete_quotes(data):
    if is_json(data):
        return data
    else:
        set_space(data)
        if data.startswith("["):
            data = cut_list(data)
            return data
        else:
            cplaces2, data, temp_data = get_temp_places(data)
            for i in range(len(cplaces2)):
                temp = cut_curly_braces(cplaces2[i], data)
                if is_json(temp):
                    pass
                else:
                    flag = True
                    while (flag):
                        if i < len(cplaces2) - 2:
                            data, cplaces2, i = method_for_places_over_two(i, cplaces2, data, temp_data)
                        elif i == len(cplaces2) - 2:
                            data = method_for_last_two_places(cplaces2, i, data, temp_data)
                            return data
                        elif i == len(cplaces2) - 1:
                            data = process_of_delete(i, cplaces2, data, temp_data, "")
                            return data
                        else:
                            flag = False
        data = join_curly_braces(cplaces2, temp_data)
        return data


def join_curly_braces(cplaces2, temp_data):
    data = ",".join(cplaces2)
    if temp_data.startswith("{"):
        data = "{" + data
    if temp_data.endswith("}"):
        data = data + "}"
    return data


def cut_curly_braces(source_data, data):
    temp = copy.deepcopy(source_data)
    if source_data.startswith("{"):
        temp = source_data[1:len(data)]
    if source_data.endswith("}"):
        temp = source_data[:len(data) - 1]
    return temp


def method_for_places_over_two(i, cplaces2, data, temp_data):
    flag2 = True
    while (flag2):
        if i < len(cplaces2) - 1:
            if not "\":" in cplaces2[i + 1]:
                cplaces2[i] = cplaces2[i][:len(cplaces2[i])] + cplaces2[i + 1]
                cplaces2.pop(i + 1)
                i = i - 1
            else:
                data = process_of_delete(i, cplaces2, data, temp_data, "")
            i = i + 1
        else:
            flag2 = False
    return data, cplaces2, i


def method_for_last_two_places(cplaces2, i, data, temp_data):
    f = len(cplaces2) - 2
    s = len(cplaces2) - 1
    if is_json("{" + cplaces2[f] + "}") and is_json("{" + cplaces2[s] + "}"):
        tempc = ""
    elif not is_json("{" + cplaces2[f] + "}") and not is_json("{" + cplaces2[s] + "}"):
        cplaces2[f] = cplaces2[f][:len(cplaces2[f]) - 1] + cplaces2[s][1:]
        tempc = cplaces2[f]
    elif is_json("{" + cplaces2[f] + "}") and not is_json("{" + cplaces2[s] + "}"):
        if not "\":" in cplaces2[s]:
            cplaces2[f] = cplaces2[f][:len(cplaces2[f]) - 1] + cplaces2[s][1:]
            tempc = f
        else:
            tempc = s
    else:
        tempc = ""
    data = process_of_delete(i, cplaces2, data, temp_data, tempc)
    return data


def set_space(data):
    if data.startswith(" "):
        for i in range(len(data)):
            if not data[i].isspace():
                space = i
                data = data[space:len(data)]
                break
    return data


def get_temp_places(data):
    temp_data = copy.deepcopy(data)
    if data.startswith("{"):
        data = data[1:len(data)]
    if data.endswith("}"):
        data = data[:len(data) - 1]
    cplaces = data.split(",")
    cplaces2 = []
    for c in cplaces:
        cplaces2.append(str(c))
    return cplaces2, data, temp_data


def cut_list(data):
    l_places = data.split(",")
    list_flag = True
    c = 0
    while (list_flag):
        if c < len(l_places):
            if l_places[c].startswith("{"):
                if l_places[c].endswith("}"):
                    temp3 = delete_quotes(l_places[c])
                    data = data.replace(l_places[c], temp3)
                    l_places[c] = temp3

                else:
                    if c < len(l_places) - 1:
                        l_places[c] = l_places[c] + "," + l_places[c + 1]
                        l_places.pop(c + 1)
                        c = c - 1
            else:
                temp2 = delete_quotes(l_places[c])
                data = data.replace(l_places[c], temp2)
            c = c + 1
        else:
            list_flag = False

    return data


def process_of_delete(i, cplaces2, data, temp_data, temp):
    kvs = cplaces2[i].split("\":")
    k = kvs[0]
    v = "\":".join(kvs[1:])
    if str(v).startswith("{"):
        if str(v).endswith("}"):
            temp2 = delete_quotes(v)
            data = data.replace(v, temp2)
            cplaces2[i] = cplaces2[i].replace(v, temp2)
        else:
            if i < len(cplaces2) - 1:
                cplaces2[i] = cplaces2[i] + ", " + cplaces2[i + 1]
                cplaces2.pop(i + 1)
                i = i - 1

    elif str(v).startswith("["):
        if str(v).endswith("]"):
            vlists = v[1:len(v) - 1].split(",")
            for vlist in vlists:
                temp2 = delete_quotes(vlist)
                if i == len(cplaces2) - 1:
                    data = data.replace(" ", "")
                    vlist = vlist.replace(" ", "")
                data = data.replace(vlist, temp2)
                cplaces2[i] = cplaces2[i].replace(vlist, temp2)
        else:
            if i < len(cplaces2) - 1:
                cplaces2[i] = cplaces2[i] + ", " + cplaces2[i + 1]
                cplaces2.pop(i + 1)
                i = i - 1
    elif str(v) == "":
        pass
    else:
        if i < len(cplaces2) - 1 and str(v).startswith("\"") and str(v).endswith("\""):
            tempk2 = copy.deepcopy(k)
            k2 = k[1:len(k)].replace("\"", "")
            v2 = v[1:len(v) - 1].replace("\"", "")
            if tempk2.startswith("{"):
                cplaces2[i] = k2 + "\":\"" + v2 + "\""
            elif tempk2.startswith("\""):
                cplaces2[i] = "\"" + k2 + "\":\"" + v2 + "\""
    if i in (len(cplaces2) - 1, len(cplaces2) - 2):
        if str(v).startswith("\"") and str(v).endswith("\""):
            k2 = k[1:len(k)].replace("\"", " ")
            v2 = v[1:len(v) - 1].replace("\"", " ")
            if i == len(cplaces2) - 2 and temp != "":
                i = temp
            cplaces2[i] = "\"" + str(k2) + "\":\"" + str(v2) + "\""
        data = ",".join(cplaces2)

        if temp_data.startswith("{"):
            data = "{" + data
        if temp_data.endswith("}"):
            data = data + "}"
    return data


def compare_size(a, b):
    if a>b or a == b:
        return True
    else:
        return False


"""
tstring = u'{"aaa":"11,1{a1","bbb":22222,"cc}c":"asdgd"s,g"rsh","dddd":"test"}'
data1 = u'{ "qudao_name":{"nam"}e":"美"金"}, "id":1, "enen":{"hap":"shad",oux"}ing"},"try":[{"id":1},{"id":3},{"id":2}], "qudao_desc": "" < p > 充值说明： < /p><pstyle=""color:red"">1、联通：面额10、20、30，单个手机日限制：50，单个手机月限制：200。</p > ","id":0,"qudao_desc": "" < p > 充值 说明： < /p><pstyle=""color:red"">1、联通：面额10、20、30，单个手机日限制：50，单个手机月限制：200。</p > ","qudao_desc": "" < p > 充值说明： < /p><pst,yle=""color:red"">1、联通：面额10、20、30，单个手机日限制：50，单个手机月限制：200。</p > "}'
testdata = u'{ "qudao_id": "9014", "qudao_name": "奇游-MyCard线上支付", "qudao_code": "9014", "qudao_fee": "0.2000",  "qudao_money_rate": "0.12",  "qudao_desc": "在线<a href=\"http://www.mycard520.com.tw/web/mc_service/mc_qa_os.aspx\" target=\"_blank\">MyCard線上客服回覆系統</a>(02)2651-0754<br />在线客服：<a href=\"http://faq.g.iqiyi.com/tp/front/service.htm\" target=\"_blank\">联系客服</a>", "qudao_status": "0", "qudao_icon": "", "display_name": "", "qudao_signatory": "5"}'
tr = to_json_string(testdata)
if is_json(tr):
    print(tr)
"""
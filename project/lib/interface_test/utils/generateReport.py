import xmltodict
import json
import copy
import re


def xml_to_json(xml_file_name):
    # 打开指定目录 文件为gb2312编码
    file_object = open(xml_file_name, encoding='utf-8')
    try:
        all_the_xmlStr = file_object.read()
    finally:
        file_object.close()
    convertedDict = xmltodict.parse(all_the_xmlStr)
    json_str = json.dumps(convertedDict, ensure_ascii=False).replace('@', '')
    j_str = json.loads(json_str,encoding='utf-8')

    return j_str


def split_url_part(xml_dict, k, single_test_case):
    if "url" in xml_dict["suite"].keys():
        url_dict = xml_dict["suite"]["url"]
        if "url_place" in url_dict.keys():
            url_place = url_dict["url_place"]
            if not url_place.endswith("?"):
                url_place = url_place + "?"
        else:
            print("请输入接口地址")
        if "response_method" in url_dict.keys():
            response_method = url_dict["response_method"]
        else:
            print("请输入接口地址")
    else:
        print ("请检查用例文件，没有url标签")

    if k == -1:
        testcase = xml_dict["suite"]["testcase"]
    else:
        testcase = xml_dict["suite"]["testcase"][k]
    if "input_parameter" in testcase.keys():
        input_parameters = testcase["input_parameter"]
        parameter = ""
        if not input_parameters == None:
            for p in input_parameters.keys():
                if input_parameters[p] == None:
                    parameter = parameter + p + "=&"
                else:
                    parameter = parameter + p + "=" + input_parameters[p] + "&"
            parameter = parameter[0:-1]
    else:
        parameter = ""

    url = url_place + parameter
    single_test_case["url_place"] = url_place
    single_test_case["url_parameter"] = parameter
    single_test_case["response_method"] = response_method
    return single_test_case


def split_testcase_part(testcase, single_test_case):
    testcase_id = testcase["id"]
    testcase_name = testcase["name"]
    if "loop" in testcase.keys():
        testcase_loop = testcase["loop"]
    else:
        testcase_loop = ""
    testcase_expect = testcase["expect"]
    expect_data = generate_key(testcase_expect)
    single_test_case["testcase_id"] = testcase_id
    single_test_case["testcase_name"] = testcase_name
    single_test_case["testcase_loop"] = testcase_loop
    return single_test_case, expect_data


def generate_key(testcase_expect):
    if isinstance(testcase_expect, dict):
        for d in testcase_expect.keys():
            # 'tag': '!', '#text': '233174820'
            testcase_expect = change_tag_flag(testcase_expect, d)
            generate_key(testcase_expect[d])
    elif isinstance(testcase_expect, list):
        for l in testcase_expect:
            generate_key(l)
    else:
        pass
    return testcase_expect


def change_tag_flag(testcase_expect, d):
    if isinstance(testcase_expect[d], dict):
        if "tag_flag" in testcase_expect[d].keys():
            tag_flag = testcase_expect[d]["tag_flag"]
            tag_value = testcase_expect[d]["#text"]
            if tag_flag == "!":
                real_value = "!" + tag_value
                if "test_type" in testcase_expect[d].keys():
                    testcase_expect[d]["#text"] = real_value
                else:
                    testcase_expect[d] = real_value
            elif tag_flag == "or":
                real_value = "$:" + tag_value
                if "test_type" in testcase_expect[d].keys():
                    testcase_expect[d]["#text"] = real_value
                else:
                    testcase_expect[d] = real_value
            elif tag_flag == "%":
                real_value = "%" + tag_value + "%"
                if "test_type" in testcase_expect[d].keys():
                    testcase_expect[d]["#text"] = real_value
                else:
                    testcase_expect[d] = real_value
    return testcase_expect


def get_expect_part_dict(expect_data):
    if isinstance(expect_data, dict):
        for d in list(expect_data):
            if isinstance(expect_data[d], dict):
                if "test_type" in expect_data[d].keys():
                    expect_data.pop(d)
                else:
                    get_expect_part_dict(expect_data[d])
            else:
                get_expect_part_dict(expect_data[d])
    elif isinstance(expect_data, list):
        flag = True
        l = 0
        while (flag):
            if l < len(expect_data):
                if isinstance(expect_data[l], dict):
                    ss = expect_data[l]
                    if "test_type" in expect_data[l].keys():
                        del expect_data[l]
                        l = l - 1
                    else:
                        get_expect_part_dict(expect_data[l])
                else:
                    get_expect_part_dict(expect_data[l])
                l = l + 1
            else:
                flag = False
    else:
        pass
    return expect_data


def check_expect_part_if_list_or_not(real_expect_data_part, del_expect_check_sort):
    if isinstance(del_expect_check_sort, dict):
        for d in del_expect_check_sort.keys():
            if d in real_expect_data_part.keys():
                if len(real_expect_data_part[d]) == 1 and isinstance(real_expect_data_part[d], list):
                    real_expect_data_part[d] = real_expect_data_part[d][0]
            else:
                continue
    return real_expect_data_part

def check_all_part_if_list_or_not(del_expect_check_sort):
    if isinstance(del_expect_check_sort, dict):
        for d in del_expect_check_sort.keys():
            if isinstance(del_expect_check_sort[d], dict):
                check_all_part_if_list_or_not(del_expect_check_sort[d])
            elif isinstance(del_expect_check_sort[d], list):
                if len(del_expect_check_sort[d]) == 1:
                    del_expect_check_sort[d] = del_expect_check_sort[d][0]
                    check_all_part_if_list_or_not(del_expect_check_sort[d])
            else:
                continue
    elif isinstance(del_expect_check_sort, list):

            for l in del_expect_check_sort:
                check_all_part_if_list_or_not(l)
    else:
        pass
    return del_expect_check_sort


def get_expect_all_expect_dicts(expect_data, single_test_case):

    expect_data_part = copy.deepcopy(expect_data)
    expect_data_part = get_expect_part_dict(expect_data_part)
    # expect_data_all 从期望中直接提取的比较全部
    merge = get_expect_all_dict(expect_data, expect_data_part)
    expect_data_all = del_empty_dict(del_empty_dict(merge))
    temp_expect_data_part = del_empty_dict(expect_data_part)

    real_expect_data_part = del_empty_dict(del_empty_dict(expect_data_part))

    del_expect_check_sort = copy.deepcopy(expect_data_all)
    #del_expect_check_sort = get_expect_part_dict1(del_expect_check_sort, "check_sort")
    del_expect_check_sort = get_expect_part_dict2(del_expect_check_sort, ["regular","check_sort","exist"])
    del_expect_check_sort = del_empty_dict(del_empty_dict(del_expect_check_sort))

    real_expect_data_part = check_expect_part_if_list_or_not(real_expect_data_part, del_expect_check_sort)
    del_expect_check_sort = check_all_part_if_list_or_not(del_expect_check_sort)
    single_test_case["expect_data_part"] = real_expect_data_part
    single_test_case["expect_data_all"] = del_expect_check_sort
    #single_test_case["expect_data_all"] = expect_all
    return single_test_case


def get_expect_all_dict(expect_data, expect_data_part):
    if isinstance(expect_data_part, dict):
        for d in list(expect_data_part):
            if d in expect_data:
                if isinstance(expect_data[d], dict):
                    get_expect_all_dict(expect_data[d], expect_data_part[d])
                elif isinstance(expect_data[d], list):
                    get_expect_all_dict(expect_data[d], expect_data_part[d])
                else:
                    if expect_data[d] == expect_data_part[d]:
                        expect_data.pop(d)
    elif isinstance(expect_data_part, list):
        for l in expect_data_part:
            for i in expect_data:
                if isinstance(i, dict):
                    get_expect_all_dict(i, l)
    else:
        pass
    return expect_data


def del_empty_dict(expect_data):

    if isinstance(expect_data, dict):

        for d in list(expect_data):
            if not expect_data[d] == None:
                if len(expect_data[d]) == 0:
                    expect_data.pop(d)
                else:
                    del_empty_dict(expect_data[d])
    elif isinstance(expect_data, list):
        flag = True
        l=0
        while(flag):
            if l < len(expect_data):
                if len(expect_data[l]) == 0:
                    expect_data.pop(l)
                    l = l-1
                else:
                    del_empty_dict(expect_data[l])
                l=l+1
            else:
                flag = False
    else:
        pass
    return expect_data


def get_expect_part_dict1(expect_data, key):
    if isinstance(expect_data, dict):
        for d in list(expect_data):
            if isinstance(expect_data[d], dict):
                if "test_type" in expect_data[d].keys() and expect_data[d]["test_type"] == key:
                    #expect_data.pop(d)
                    pass
                elif "test_type" in expect_data[d].keys() and expect_data[d]["test_type"] != key:
                    if not expect_data[d]["test_type"] == "check_sort":
                        del expect_data[d]["test_type"]
                    if "#text" in expect_data[d]:
                        expect_data[d] = expect_data[d]["#text"]
                    get_expect_part_dict1(expect_data[d], key)
                else:
                    get_expect_part_dict1(expect_data[d], key)
            else:
                get_expect_part_dict1(expect_data[d], key)
    elif isinstance(expect_data, list):
        flag = True
        l = 0
        while (flag):
            if l < len(expect_data):
                if isinstance(expect_data[l], dict):
                    if "test_type" in expect_data[l].keys() and expect_data[l]["test_type"] == key:
                        #del expect_data[l]
                        #l = l - 1
                        pass
                    elif "test_type" in expect_data[l].keys() and expect_data[l]["test_type"] != key:
                        if not expect_data[l]["test_type"] == "check_sort":
                            del expect_data[l]["test_type"]
                        if "#text" in expect_data[l]:
                            expect_data[l] = expect_data[l]["#text"]
                        get_expect_part_dict1(expect_data[l], key)
                    else:
                        get_expect_part_dict1(expect_data[l], key)
                else:
                    get_expect_part_dict1(expect_data[l], key)
                l = l + 1
            else:
                flag = False
    else:
        pass
    return expect_data


def get_expect_part_dict2(expect_data, key):
    if isinstance(expect_data, dict):
        for d in list(expect_data):
            if isinstance(expect_data[d], dict):
                if "test_type" in expect_data[d].keys() and expect_data[d]["test_type"] in key:
                    #expect_data.pop(d)
                    pass
                elif "test_type" in expect_data[d].keys() and expect_data[d]["test_type"] not in key:
                    if not expect_data[d]["test_type"] == "check_sort":
                        del expect_data[d]["test_type"]
                    if "#text" in expect_data[d]:
                        expect_data[d] = expect_data[d]["#text"]
                        get_expect_part_dict2(expect_data[d], key)
                else:
                    get_expect_part_dict2(expect_data[d], key)
            else:
                get_expect_part_dict2(expect_data[d], key)
    elif isinstance(expect_data, list):
        flag = True
        l = 0
        while (flag):
            if l < len(expect_data):
                if isinstance(expect_data[l], dict):
                    if "test_type" in expect_data[l].keys() and expect_data[l]["test_type"] in key:
                        #del expect_data[l]
                        #l = l - 1
                        pass
                    elif "test_type" in expect_data[l].keys() and expect_data[l]["test_type"] not in key:
                        #if not expect_data[l]["test_type"] in "check_sort":
                            #del expect_data[l]["test_type"]
                        if "#text" in expect_data[l]:
                            expect_data[l] = expect_data[l]["#text"]
                            get_expect_part_dict2(expect_data[l], key)
                    else:
                        get_expect_part_dict2(expect_data[l], key)
                else:
                    get_expect_part_dict2(expect_data[l], key)
                l = l + 1
            else:
                flag = False
    else:
        pass
    return expect_data


def get_test_case_content(xml_dict):
    single_test_case = {}
    test_case_list = []
    if "testcase" in xml_dict["suite"]:
        if isinstance(xml_dict["suite"]["testcase"], dict):
            single_test_case = split_url_part(xml_dict, -1, single_test_case)
            single_test_case, expect_data = split_testcase_part(xml_dict["suite"]["testcase"], single_test_case)
            single_test_case = get_expect_all_expect_dicts(expect_data, single_test_case)
            test_case_list.append(single_test_case)
        elif isinstance(xml_dict["suite"]["testcase"], list):
            for t in range(len(xml_dict["suite"]["testcase"])):
                single_test_case = split_url_part(xml_dict, t, single_test_case)
                single_test_case, expect_data = split_testcase_part(xml_dict["suite"]["testcase"][t], single_test_case)
                single_test_case = get_expect_all_expect_dicts(expect_data, single_test_case)
                single_test_case_copy = copy.deepcopy(single_test_case)
                test_case_list.append(single_test_case_copy)
    else:
        print("请输入testcase")
    return test_case_list


def get_check_sort_part(expect_data):
    if isinstance(expect_data, dict):
        for d in expect_data.keys():
            if isinstance(expect_data[d], dict) or isinstance(expect_data[d], list):
                return get_check_sort_part(expect_data[d])
            elif d == "test_type" and expect_data["test_type"] == 'check_sort':
                s = 'check_sort:'+ expect_data['keyword'] + "||" + expect_data['order'] +"||"
                return s
            else:
                continue
    elif isinstance(expect_data, list):
        for l in expect_data:
            return get_check_sort_part(l)


def get_special_check_part(expect_data, key):
    if isinstance(expect_data, dict):
        for d in list(expect_data):
            if isinstance(expect_data[d], dict):
                if "test_type" in expect_data[d].keys() and expect_data[d]["test_type"] == key:
                    expect_data.pop(d)
                else:
                    get_special_check_part(expect_data[d], key)
            else:
                get_special_check_part(expect_data[d], key)
    elif isinstance(expect_data, list):
        flag = True
        l = 0
        while (flag):
            if l < len(expect_data):
                if isinstance(expect_data[l], dict):
                    if "test_type" in expect_data[l].keys() and expect_data[l]["test_type"] == key:
                        del expect_data[l]
                        l = l - 1
                        pass
                    else:
                        get_special_check_part(expect_data[l], key)
                else:
                    get_special_check_part(expect_data[l], key)
                l = l + 1
            else:
                flag = False
    else:
        pass

    return expect_data


def get_special_check_part_content(expect_data, key):
    if isinstance(expect_data, dict):
        for d in list(expect_data):
            if isinstance(expect_data[d], dict):
                if "test_type" in expect_data[d].keys() and expect_data[d]["test_type"] != key:
                    expect_data.pop(d)
                else:
                    get_special_check_part_content(expect_data[d], key)
            else:
                get_special_check_part_content(expect_data[d], key)
    elif isinstance(expect_data, list):
        flag = True
        l = 0
        while (flag):
            if l < len(expect_data):
                if isinstance(expect_data[l], dict):
                    if "test_type" in expect_data[l].keys() and expect_data[l]["test_type"] != key:
                        del expect_data[l]
                        l = l - 1
                        pass
                    else:
                        get_special_check_part_content(expect_data[l], key)
                else:
                    get_special_check_part_content(expect_data[l], key)
                l = l + 1
            else:
                flag = False
    else:
        pass

    return expect_data


def get_sort_and_all_part(data_all):
    s = get_check_sort_part(data_all)
    data_all = get_special_check_part(data_all, "check_sort")
    data_all = del_empty_dict(data_all)
    return s, data_all


def adjust_key_number_or_not(key):
    temp_list = re.compile(r'^game_id_[0-9]+$').findall(key)
    if len(temp_list) > 0:
        return temp_list[0]
    else:
        return False


def transfer_special_number_key(test_case_list, new_test_case_list):
    if isinstance(test_case_list, dict):
        for d in test_case_list.keys():
            adjust_result = adjust_key_number_or_not(d)
            if not adjust_result == False:
                new_id = adjust_result.split("_")[-1]
                new_test_case_list[new_id] = test_case_list[d]
                del new_test_case_list[d]
                transfer_special_number_key(test_case_list[d], new_test_case_list[new_id])
            else:
                transfer_special_number_key(test_case_list[d], new_test_case_list[d])
    elif isinstance(test_case_list, list):
        for l in range(len(test_case_list)):
            transfer_special_number_key(test_case_list[l], new_test_case_list[l])
    else:
        pass
    return new_test_case_list

def get_test_cases(file):
    xml_file_name = file
    xml_dict = xml_to_json(xml_file_name)
    test_case_list = get_test_case_content(xml_dict)
    new_test_case_list = copy.deepcopy(test_case_list)
    test_case_list = transfer_special_number_key(test_case_list, new_test_case_list)
    return test_case_list


def get_special_part_dict(all_data, key):
    t_data_all = copy.deepcopy(all_data)
    t_data_all = get_special_check_part_content(t_data_all, key)
    t_data_all2 = copy.deepcopy(all_data)
    expect_data_part = copy.deepcopy(all_data)
    expect_data_part = get_expect_part_dict(expect_data_part)
    special_part_dict = get_expect_all_dict(t_data_all, expect_data_part)
    other_part = get_special_check_part(t_data_all2, key)
    return special_part_dict, other_part


def get_all_special_parts(single_test_case):
    s, all_data = get_sort_and_all_part(single_test_case["expect_data_all"])
    exist_part, other_part = get_special_part_dict(all_data, "exist")
    regular_part, other_part = get_special_part_dict(other_part, "regular")
    exist_part = del_empty_dict(exist_part)
    regular_part = del_empty_dict(regular_part)
    other_part = del_empty_dict(other_part)
    return s, regular_part, exist_part, other_part


"""
file = 'D:/test/auto/code/ipecker/project/script/interface_test/houtai/card_cardlist.xml'
test_case_list = get_test_cases(file)
print(test_case_list)


data = {'data': []}
data = del_empty_dict(del_empty_dict(data))
print(data)
s = data
"""
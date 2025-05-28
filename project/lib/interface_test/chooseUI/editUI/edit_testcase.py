# -*- coding: UTF-8 -*-

"""
File Name:      edit_testcase
Author:         xumohan
Create Date:    2018/7/31
"""
import xmltodict
import json
import copy
import os

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

def change_line_to_new_order(line_list):
    i = len(line_list) - 1
    new_line_list = []
    while i>= 0:
        new_line_list.append(line_list[i])
        i -= 1
    return new_line_list

def test_case_xml_to_dict(line_list, final_path):
    path_list = change_line_to_new_order(line_list)
    for pl in path_list:
        final_path = os.path.join(final_path, pl)
    final_path = final_path[:-3] + ".xml"
    testcase_dict = xml_to_json(final_path)
    return testcase_dict, final_path
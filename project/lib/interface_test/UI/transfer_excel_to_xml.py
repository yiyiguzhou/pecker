# -*- coding: utf-8 -*-

"""
File Name:      transfer_excel_to_xml
Author:         xumohan
Create Date:    2018/7/9
C:\\Users\\xumuhan_sx\\Desktop\\exceltoxml.xlsx
"""

import re
import json
import os
from framework.utils.openpyxl import load_workbook
from xml.dom.minidom import Document


def add_child(child_name, childname_text, father_node, flag):
    doc = Document()
    child_name_temp = re.compile(r'^[0-9]+$').findall(child_name)
    if len(child_name_temp) > 0:
        new_child_name = "game_id_" + str(child_name)
    else:
        new_child_name = child_name
    child_node = doc.createElement(new_child_name)
    if flag == True:
        if not child_name == "check_sort_in_program":
            child_node.setAttribute("cmp_method", "all")
    if isinstance(childname_text, int):
        child_node_text_string = str(childname_text)
    else:
        child_node_text_string = childname_text
    child_node_text = doc.createTextNode(str(child_node_text_string))
    child_node.appendChild(child_node_text)
    father_node.appendChild(child_node)
    return  father_node


def add_url_part(sheet):
    doc = Document()
    url = doc.createElement("url")
    web_sites = sheet["D2"].value
    if str(web_sites).endswith("?"):
        web_sites = web_sites[:-1]
    web_places = web_sites.split("/")
    url_name_text = web_places[-2] + "_" + web_places[-1]
    url = add_child("url_name", url_name_text, url, False)
    url = add_child("url_place", sheet["D2"].value, url, False)
    if not sheet["G2"].value == None:
        response_method_text = sheet["G2"].value

    url = add_child("response_method", response_method_text, url, False)
    return url


def add_test_case_part(sheet, expect, row_id):

    if not sheet["F" + str(row_id)].value == None:
        expect_data_g = '{"data":' + sheet["F" + str(row_id)].value + "}"
        expect_data_g_dict = eval(expect_data_g)
        expect = split_expect(expect_data_g_dict, expect, expect, "g")

    if not sheet["G" + str(row_id)].value == None:
        expect_data_t_text = sheet["G" + str(row_id)].value
        if str(expect_data_t_text).startswith("checkSort:"):
            order_key, order, expect_data_t_text = str(expect_data_t_text)[10:].split("||")
            temp_order_dict = {}
            temp_order_dict["check_sort_in_program"] = {}
            temp_order_dict["check_sort_in_program"]["keyword"] = order_key
            temp_order_dict["check_sort_in_program"]["order"] = order
            temp_order_dict_string = json.dumps(temp_order_dict)
            if not expect_data_t_text == "":
                new_expect_data_t_text = expect_data_t_text[:-1] + "," + temp_order_dict_string[1:]
                expect_data_t = '{"data":' + new_expect_data_t_text + "}"
            else:
                expect_data_t = '{"data":' + temp_order_dict_string + "}"
        else:
            expect_data_t = '{"data":' + str(sheet["G" + str(row_id)].value) + "}"
        expect_data_t_dict = eval(expect_data_t)
        expect = split_expect(expect_data_t_dict, expect, expect, "t")

    return expect


def split_expect(expect_data, father_node, child_node, t_or_g):
    doc = Document()
    if isinstance(expect_data, dict):
        for d in expect_data.keys():
            if isinstance(expect_data[d], dict):
                father_node = child_node

                child_name_temp = re.compile(r'^[0-9]+$').findall(d)
                if len(child_name_temp) > 0:
                    new_d = "game_id_" + str(d)
                else:
                    new_d = d
                child_node = doc.createElement(new_d)
                if d == "check_sort_in_program":
                    child_node.setAttribute("cmp_method","check_sort")
                split_expect(expect_data[d], father_node, child_node, t_or_g)
                father_node.appendChild(child_node)
            elif isinstance(expect_data[d], list):
                father_node = child_node
                child_name_temp = re.compile(r'^[0-9]+$').findall(d)
                if len(child_name_temp) > 0:
                    new_d = "game_id_" + str(d)
                else:
                    new_d = d
                child_node = doc.createElement(new_d)
                split_expect(expect_data[d], father_node, child_node, t_or_g)
                father_node.appendChild(child_node)
            else:
                if t_or_g == "t" and child_node.nodeName == "check_sort_in_program":
                    child_node = add_child(d, expect_data[d], child_node, False)
                elif t_or_g == "t":
                    child_node = add_child(d, expect_data[d], child_node, True)
                else:
                    child_node = add_child(d, expect_data[d], child_node, False)
                father_node.appendChild(child_node)

    elif isinstance(expect_data, list):
        for l in expect_data:
            if isinstance(l, dict):
                split_expect(l, father_node, child_node, t_or_g)
                father_node.appendChild(child_node)
            else:
                pass
    else:
        pass

    return father_node


def delete_empty(parameters):
    if not parameters == None:
        paras = parameters.split("&")
        flag = True
        i = 0
        while (flag):
            if i < len(paras):
                if str(paras[i]).endswith("="):
                    paras.pop(i)
                    i -= 1
                i += 1
            else:
                flag = False
    else:
        paras = []
    return paras


def excel_to_xml(workbook_name, test_group):
    #wbs = ["E:\\桌面备份\\接口测试\\一些用例\\会员\\生产系统.xlsx","E:\\桌面备份\\接口测试\\一些用例\\会员\\用户系统.xlsx","E:\\桌面备份\\接口测试\\一些用例\\会员\\支付系统.xlsx"]
    wb = load_workbook(workbook_name)
    sheetnames = wb.sheetnames
    path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    new_path = os.path.join(path, "script")
    interface_test_path = os.path.join(new_path, "interface_test")
    for sheetname in sheetnames:

        doc = Document()
        sheet = wb[sheetname]

        web_sites = sheet["D2"].value
        if str(web_sites).endswith("?"):
            web_sites = web_sites[:-1]
        web_places = web_sites.split("/")
        url_name_text = web_places[-2] + "_" + web_places[-1]
        file_dir_path = os.path.join(interface_test_path, test_group)
        file_path = url_name_text + ".xml"
        file_name = os.path.join(file_dir_path, file_path)
        try:

            print(url_name_text)
            if os.path.exists(file_name):
                os.remove(file_name)
            file = open(file_name, 'w', encoding='utf-8')
            file.close()

            suit = doc.createElement('suite')
            suit.setAttribute("shelf", url_name_text)
            doc.appendChild(suit)
            max_column = sheet.max_column
            max_row = sheet.max_row
            for row in range(sheet.max_row):
                if row == 0:
                    url = add_url_part(sheet)
                    suit.appendChild(url)
                else:
                    row_id = row+1
                    ss = "A" + str(row_id)
                    num = sheet["A" + str(row_id)].value
                    test_point = sheet["B" + str(row_id)].value
                    parameters = sheet["E" + str(row_id)].value
                    expect_code = sheet["F" + str(row_id)].value
                    testcase = doc.createElement("testcase")
                    testcase.setAttribute("id", str(num))
                    testcase.setAttribute("name", str(test_point))
                    paras = delete_empty(parameters)
                    input_parameter = doc.createElement("input_parameter")
                    try:
                        for p in paras:
                            tag_name, tag_text = p.split("=")
                            input_parameter = add_child(tag_name, tag_text, input_parameter, False)
                    except:
                        print(num, p)
                    testcase.appendChild(input_parameter)
                    expect = doc.createElement("expect")
                    expect = add_child("code", expect_code, expect, False)
                    testcase.appendChild(expect)
                    suit.appendChild(testcase)
                #suit.appendChild(testcase)
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(doc.toprettyxml())

        except:
            print("Fail------", url_name_text, "------Fail")


workbook_name = "C:\\Users\\xumuhan_sx\\Desktop\\interface.xlsx"
test_group = "testUI"
excel_to_xml(workbook_name, test_group)

# -*- coding: UTF-8 -*-

"""
File Name:      save_new_testcase_xml
Author:         xumohan
Create Date:    2018/8/2
"""
import os
from xml.dom.minidom import Document


doc = Document()

def generate_xml_tree(testcase_dict, father_node):

    if isinstance(testcase_dict, dict):
        for d in testcase_dict.keys():
            if isinstance(testcase_dict[d], dict):
                child_node = doc.createElement(d)
                father_node.appendChild(child_node)
                generate_xml_tree(testcase_dict[d], child_node)
            elif isinstance(testcase_dict[d], list):
                for l in testcase_dict[d]:
                    child_node = doc.createElement(d)
                    father_node.appendChild(child_node)
                    generate_xml_tree(l, child_node)
            else:
                child_node = doc.createElement(d)
                if testcase_dict[d] == None:
                    text_node = doc.createTextNode("")
                else:
                    text_node = doc.createTextNode(testcase_dict[d])
                child_node.appendChild(text_node)
                father_node.appendChild(child_node)
    elif isinstance(testcase_dict, list):
        for tl in testcase_dict:
            generate_xml_tree(tl, father_node)
    else:
        pass
    return father_node

def save_edit_xml(testcase_dict, file_name):
    doc_tree = generate_xml_tree(testcase_dict, doc)
    if os.path.exists(file_name):
        os.remove(file_name)
    file = open(file_name, 'w', encoding='utf-8')
    file.write(doc_tree.toprettyxml())
    file.close()



"""
testcase_dict = {'suite': {'shelf': 'UGameList_listByGameOnlineDate', 'url': {'url_name': 'UGameList_listByGameOnlineDate', 'url_place': 'http://apisgame.qiyi.domain/product/unified/UGameList/listByGameOnlineDate?', 'response_method': 'GET'}, 'testcase': [{'id': '4', 'name': '查询所有PC_WEB网络游戏列表', 'input_parameter': {'page': '1', 'page_size': '5', 'network': '1', 'terminal': '4', 'source': '1', 'sign': '3e32d7887cb190de855296540568eb5c'}, 'expect': {'code': '200'}}, {'id': '5', 'name': '查询发行区域为大陆的所有游戏列表', 'input_parameter': {'publish_area': '1', 'source': '1', 'sign': '6dd7d83fdbbb063f387f7c79c8f91e1c'}, 'expect': {'code': '200'}}, {'id': '6', 'name': '查询支付状态开启的游戏的所有游戏列表', 'input_parameter': {'pay_status': '1', 'source': '1', 'sign': '9cab7ac1695f58391f2e7f4ebdb51faf'}, 'expect': {'code': '200'}}, {'id': '7', 'name': '查询已上线的所有游戏', 'input_parameter': {'online_status': '1', 'source': '1', 'sign': '0bdd48f31c91632d5389251fae81f0de'}, 'expect': {'code': '200'}}, {'id': '8', 'name': '模糊搜索(name只能是数字，字母，中文字符的组合)', 'input_parameter': {'name': 'a', 'source': '1', 'sign': 'e033d86f1f070448e9c0b078431acd0d'}, 'expect': {'code': '200'}}, {'id': '9', 'name': '模糊搜索输入特殊字符，接口返回错误响应码', 'input_parameter': {'name': '--', 'source': '1', 'sign': '44de434eb502c28e2b4657512c76190b'}, 'expect': {'code': '10001'}}, {'id': '10', 'name': '请求参数page*page_size等于100', 'input_parameter': {'page': '1', 'page_size': '100', 'source': '1', 'sign': 'a889b690f1824870c70ecd6acac38735'}, 'expect': {'code': '200'}}, {'id': '11', 'name': '请求参数page*page_size大于100', 'input_parameter': {'page': '1', 'page_size': '101', 'source': '1', 'sign': 'b79db20658b6f8277687ea5f35b82b81'}, 'expect': {'code': '10001'}}, {'id': '12', 'name': '请求参数page=0，接口返回错误响应码', 'input_parameter': {'page': '0', 'page_size': '10', 'source': '1', 'sign': 'e943350054cc8b825ea8b2d05723e9f3'}, 'expect': {'code': '10001'}}, {'id': '13', 'name': '请求参数page_size=0，接口返回错误响应码', 'input_parameter': {'page': '1', 'page_size': '0', 'source': '1', 'sign': '6dcd99491feee4a147fc6b43247a9d3f'}, 'expect': {'code': '10001'}}]}}
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
new_path = os.path.join(path, "project")
file_name = os.path.join(new_path, "test_test_test_temp_xml.xml")

save_edit_xml(testcase_dict, file_name)
"""
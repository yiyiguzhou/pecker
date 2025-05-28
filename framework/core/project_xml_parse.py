# -*- coding: UTF-8 -*-

"""
File Name:      project_xml_parse
Author:         zhangwei04
Create Date:    2017/12/25
"""

import re
import xml.etree.ElementTree as ET
from framework.core.resource import g_resource, OrderSet


def project_xml_parser():
    """xml解析函数
    """
    data_dict = g_resource['xml_data']  # 存放xml信息字典
    input_dict = g_resource['input_args']

    tree = ET.parse(input_dict['xml'])
    root = tree.getroot()

    data_dict['loop'] = abs(int(root.get("loop", "1")))
    order = root.get("order", "normal")
    if order in OrderSet().values:
        data_dict['order'] = order

    # 获取用例信息列表，存储单元为(testcase, loop)
    testcase_info_list = []
    testcase_set = set()

    for child in root:
        if child.text:
            child_info = (__testcase_path_type_parse(child.text),)
            child_info += (abs(int(child.get("loop", "1"))),)
            if child.text not in testcase_set:  # 去掉重复用例
                testcase_set.add(child.text)
                testcase_info_list.append(child_info)
    data_dict['testcase'] = testcase_info_list


def __testcase_path_type_parse(case_path):
    """
    用例配置方式适配
    Args:
        case_path: 工程文件用例配置信息，路径或者id配置
    Returns:
        转换后的用例路径
    """
    case_path_split = re.split(r"/|\\", case_path)
    if len(case_path_split) == 1:   # 使用用例id配置方式：id命名规则 业务线_终端_业务模块+编号
        case_path_split = re.split(r"_", case_path)

    return "/".join(case_path_split)


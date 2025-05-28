# -*- coding: UTF-8 -*-

"""
File Name:      testcase_data_parse
Author:         zhangwei04
Create Date:    2018/1/24
"""
import os
import xml.etree.ElementTree as ET


class TestCaseData(object):
    """
    测试用例参数类
    """
    def __init__(self, data_path_file):
        self.__load_data(data_path_file)

    def __load_data(self, data_path_file):
        """
        加载用例配置文件参数数据
        Args:
            data_path_file:用例参数配置文件路径
        """
        if data_path_file:
            xml_path = os.path.abspath(data_path_file)
            if os.path.exists(xml_path):
                self.__parse_xml_data(xml_path)

    def __parse_xml_data(self, xml_path):
        """
        通过用例名读取同名的参数配置文件
        Args:
            xml_path: 用例xml文件路径
        """
        tree = ET.parse(xml_path)
        root = tree.getroot()

        self.__walk_element(root)

    def __walk_element(self, root_node):
        """
        遍历参数元素，并添加到数据类中
        Args:
            root_node: 用例xml文件根节点
        """
        second_eles = root_node.getchildren()
        for second_ele in second_eles:
            if second_ele.tag.lower() in ('paramater', 'paramaters'):
                for param_ele in second_ele.getchildren():
                    if param_ele.text is None:  # 待确认是否不配参数时，变量是否读取
                        param_ele.text = ""
                    self.__add_parameter(param_ele)

    def __add_parameter(self, ele):
        """
        添加用例参数属性
        Args:
            ele: 用例参数节点
        """
        if hasattr(self, ele.tag):
            exist_param = getattr(self, ele.tag)
            if isinstance(exist_param, list):
                exist_param.append(ele.text)
            else:
                self.__setattr__(ele.tag, [exist_param, ele.text])
        else:
            self.__setattr__(ele.tag, ele.text)

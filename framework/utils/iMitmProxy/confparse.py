# -*- coding: UTF-8 -*-

"""
File Name:      confparse
Author:         zhangwei04
Create Date:    2018/7/23
"""
import os
import xml.etree.ElementTree as ET


class ConfParse(object):
    """
    xml配置文件解析类
    """
    def __init__(self, data_path_file):
        self.data = self.__load_data(data_path_file)

    def __load_data(self, data_path_file):
        """
        加载用例配置文件参数数据
        Args:
            data_path_file:配置文件路径
        """
        if data_path_file:
            xml_path = os.path.abspath(data_path_file)
            if os.path.exists(xml_path):
                return self.__parse_xml_data(xml_path)
        else:
            return None

    def __parse_xml_data(self, xml_path):
        """
        通过用例名读取同名的参数配置文件
        Args:
            xml_path: xml文件路径
        """
        tree = ET.parse(xml_path)
        root = tree.getroot()
        data = {}
        self.__walk_element(root, data)
        return data

    def __walk_element(self, parent_node, data):
        """
        遍历参数元素，并添加到数据类中
        Args:
            parent_node: 用例xml文件根节点
        """
        childrens = parent_node.getchildren()
        if not childrens:
            data[parent_node.tag] = parent_node.text
            return
        for child_node in childrens:
            if child_node.getchildren():
                data_dict = {}
                if child_node.tag in data:
                    if isinstance(data[child_node.tag], dict):
                        data[child_node.tag] = [data[child_node.tag]]
                    data[child_node.tag].append(data_dict)
                else:
                    data[child_node.tag] = data_dict

                self.__walk_element(child_node, data_dict)
            else:
                if child_node.tag in data:
                    if isinstance(data[child_node.tag], list):
                        data[child_node.tag].append(child_node.text)
                    else:
                        data[child_node.tag] = [data[child_node.tag], child_node.text]
                else:
                    data[child_node.tag] = child_node.text


if __name__ == "__main__":
    confparse = ConfParse("pingBack.xml")
    print(confparse.data)
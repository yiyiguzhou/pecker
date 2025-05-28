# -*- coding: UTF-8 -*-

"""
File Name:      device_aml_parse
Author:         zhangwei04
Create Date:    2017/12/25
"""

from framework.core.resource import g_resource
import xml.etree.ElementTree as ET


def device_aml_parser():
    """解析工程xml配置文件
    """
    data_dict = g_resource['aml_data']
    input_dict = g_resource['input_args']

    tree = ET.parse(input_dict['aml'])
    root = tree.getroot()

    for child in root:
        data_dict[child.tag] = {}
        if child.tag == 'device':
            for device in child:
                device_dict = {}
                data_dict[child.tag][device.tag] = device_dict
                for dev_parmter in device:
                    if dev_parmter.text:
                        device_dict[dev_parmter.tag] = dev_parmter.text
        else:
            if child.tag == 'environment':  # 环境配置使用有序字典
                import collections
                data_dict[child.tag] = collections.OrderedDict()
            for second_child in child:
                data_dict[child.tag][second_child.tag] = second_child.text
    pass
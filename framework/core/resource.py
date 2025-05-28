# -*- coding: UTF-8 -*-

"""
File Name:      resource
Author:         zhangwei04
Create Date:    2017/12/25
"""
# from enum import Enum
import platform
from framework.core.const import Const


def __get_system():
    system = platform.system()
    sys_const = {'Windows': const.SYSTEM_WINDOWS,
                 'Linux': const.SYSTEM_LINUX,
                 'Darwin': const.SYSTEM_MAC}
    return sys_const.get(system)


# 常量
const = Const()

# 资源变量
g_resource = {
    'input_args': {},
    'xml_data': {},
    'aml_data': {},
    'framework_path': None,
    'project_path': None,
    'start_time': None,
    'end_time': None,
    'log_path': None,
    'testsuite_log_dir': None,
    'testcase_log_dir': None,
    'testcase_loop': None,
    'system': __get_system(),
    'device_list': [],
    'targets': []
}

MESSAGE = []


# 集合定义
class Set(object):
    """集合类模板定义
    Attributes:
        values: 返回范围集合
    """
    def __init__(self, set_data=None):
        self.__set_data = set_data

    @property
    def values(self):
        """集合属性
        Returns:
            定义的集合
        """
        return self.__set_data


class OrderSet(Set):
    """框架执行顺序集合类
    """
    def __init__(self):
        super(OrderSet, self).__init__(("normal", "auto", "random"))


class DeviceSet(Set):
    """设备类型集合类
    """
    def __init__(self):
        super(DeviceSet, self).__init__(("android", "ios", "pc"))


if __name__ == '__main__':
    a = OrderSet()
    print(a.values)
    if 'normal' in OrderSet().valuess:
        print("yes")
    for o in OrderSet().valuess:
        print(o)

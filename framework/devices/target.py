# -*- coding: UTF-8 -*-

"""
File Name:      target
Author:         zhangwei04
Create Date:    2018/1/9
"""

import os
from framework.utils.func import introspect
from framework.core.resource import g_resource, DeviceSet
from framework.exception.exception import DevicesTypeError


class Target(object):
    """
    目标管理类，此类在设备配置文件中配置, 在用例文件中使用. 用于调用工程lib编写的用例接口，
        及加载设备类并使用设备类进行通讯
    """
    def __init__(self, name, data):
        self.device = None
        self.data = data
        self.name = name
        self.lib_path = ""

    def init(self):
        """
        初始化操作，包含加载设备操作
        Returns:

        """
        data = self.data
        self.lib_path = os.path.join(g_resource['project_path'], 'lib', data.get('lib').replace("/", '.').replace("\\", "."))
        device_type = data.get('type', "")
        if device_type not in DeviceSet().values:
            raise DevicesTypeError("cant not find type:{}".format(device_type))
        # 加载设备
        device_path = os.path.join(g_resource['framework_path'], 'devices', device_type, device_type)
        device_cls = introspect(device_path, '__device__')
        self.device = device_cls(self)

    def __getattr__(self, item):
        """
        获取属性接口，实例化工程文件的lib模块内的对象，以便调用对应的业务接口
        Args:
            item:

        Returns:

        """
        if self.device and not self.device.inited:
            self.device.init()
        # 获取属性

        item_module = ".".join([self.lib_path, item.lower(), item.lower()])
        # lib路径非lib开头，添加lib前置路径
        lib_path = self.data.get('lib').replace(".", "/")
        if not lib_path.startswith("lib"):
            lib_path = os.path.join('lib', lib_path)

        path = os.path.join(g_resource['project_path'], lib_path, item.lower())
        if not os.path.exists(path):
            item_module = ".".join([self.lib_path, item.lower()])
        cls = introspect(item_module, item)
        ins = cls(self)
        setattr(self, item, ins)
        return ins


def test(s):
    print("this is test method；%s" % s)


if __name__ == "__main__":
    devices_info = {'DUT': {'type': 'android', 'lib': 'lib/sdk', 'id': '123456789'},
     'DUT1': {'type': 'android', 'lib': 'lib/gamecenter', 'id': '321654987'}}
    t = Target('dut', 'test')
    print(t)
    t.device
    t.test("sdf")
    t.test("gdf")
    t.test("sdfasfd")
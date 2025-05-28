# -*- coding: UTF-8 -*-

"""
File Name:      target_manager
Author:         zhangwei04
Create Date:    2018/1/9
"""
from framework.devices.target import Target
from framework.core.resource import g_resource


class TargetManager(object):
    """设备管理类"""
    def __init__(self, device_data):
        self.data = device_data
        self.targets = g_resource['targets']

    def load_target(self):
        """加载Target"""
        if self.data:
            for name, target_info in self.data.items():
                target = Target(name, target_info)
                target.init()
                __builtins__[name] = target
                self.targets.append(target)

    def remove_target(self):
        """移除Target"""
        for target in self.targets:
            if hasattr(target.device, 'teardown'):
                target.device.teardown()


if __name__ == "__main__":
    data = {'DUT': {'type': 'android', 'lib': 'lib/sdk', 'id': '123456789'}, 'DUT1': {'type': 'android', 'lib': 'lib/gamecenter', 'id': '321654987'}}
    tag_mangager = TargetManager(data)

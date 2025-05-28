# -*- coding: UTF-8 -*-

"""
File Name:      base_devices
Author:         zhangwei04
Create Date:    2019/7/12
"""
from .base_device import BaseDevice


class BaseDeviceSelenium(BaseDevice):
    """
    基本设备类
    """
    def __init__(self):
        super(BaseDeviceSelenium, self).__init__()
        self._init_flag = False

    def init(self):
        """基类初始化操作，启动Appium Server及生成Session"""
        pass

    def teardown(self):
        """设备类资源释放操作"""
        pass

    @property
    def inited(self):
        """
        设备是否初始化标志
        Returns:
            设备是否初始化
        """
        return self._init_flag
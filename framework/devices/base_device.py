# -*- coding: UTF-8 -*-

"""
File Name:      base_devices
Author:         zhangwei04
Create Date:    2018/1/8
"""
from abc import ABCMeta, abstractmethod


class BaseDevice(metaclass=ABCMeta):
    """
    基本设备类
    """
    def __init__(self):
        super(BaseDevice, self).__init__()
        self._init_flag = False

    @abstractmethod
    def init(self):
        """基类初始化操作，启动Appium Server及生成Session"""
        pass

    @abstractmethod
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
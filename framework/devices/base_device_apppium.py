# -*- coding: UTF-8 -*-

"""
File Name:      base_devices
Author:         zhangwei04
Create Date:    2018/1/8
"""
import os
from framework.utils.appium.remote import AppiumRemote
from framework.utils.appium.appium_server import AppiumServer
from framework.utils.appium.base_api import BaseApi as AppiumApi
from framework.core.resource import g_resource
from framework.exception.exception import DeviceNotFound

from .base_device import BaseDevice


class BaseDeviceAppium(BaseDevice, AppiumApi):
    """
    基本设备类，Andorid及IOS设备的基类，用于两种设备通用操作的定义及实现
    """
    def __init__(self, target):
        super(BaseDeviceAppium, self).__init__()
        self.target = target
        self.data = target.data
        self.id = self.data.get('id', None)
        self.desired_caps = {}
        self.appium_server = None
        self._init_flag = False
        self.__is_log_start = False
        self.__identity_device_flag = False     # 设备是否已经检测过，若已经检测过，则置True

    def init(self):
        """
        基类初始化操作，启动Appium Server及生成Session
        """
        self.appium_server = AppiumServer(os.path.join(g_resource['log_path'], '{}_appium_log.txt').format(self.target.name))
        self.appium_server.start()
        self._connect_server()
        self._collect_environment()

    def _start_dev_log(self):
        """
        开启抓取设备日志
        """
        self.__is_log_start = True

    def _stop_dev_log(self):
        """
        停止抓取设备日志
        """
        self.__is_log_start = False

    def _connect_server(self):
        """
        启Session连接Appium Server
        """
        self.driver = AppiumRemote(self.appium_server.url, self.desired_caps)

    def start_log(self):
        """开启用例设备日志"""
        pass

    def stop_log(self):
        """停止用例设备日志"""
        pass

    def teardown(self):
        """
        设备类资源释放操作
        """
        if self.driver:
            self.driver.quit()

        if self.appium_server:
            self.appium_server.stop()

    def use_device(self):
        """
        通过配置文件配置的id和实际获取的id list比较，若id不正确则抛出异常
        Raises:
            DeviceNotFound：设备没找到异常

        """
        if self.__identity_device_flag:
            return True
        self.__identity_device_flag = True

        dev_list = g_resource['device_list']
        for dev_info in dev_list:
            if self.id and dev_info.get('id') == self.id and dev_info.get('status') == 'candidate':
                dev_info['status'] = 'used'
                return True
            elif not self.id and dev_info.get('status') == 'free':
                self.id = dev_info.get('id')
                dev_info['status'] = 'used'
                return True
            else:
                pass

        # 若设配没有匹配到，则抛出设备没找到异常
        err_msg = "device: {} cant be not found".format(self.id if self.id else '')
        raise DeviceNotFound(err_msg)

    @property
    def inited(self):
        """
        设备是否初始化标志
        Returns:
            设备是否初始化
        """
        return self._init_flag

    def _collect_environment(self):
        """收集设备信息，并回填到环境字典中"""
        pass



    # def is_dev_free_status(self):
    #     dev_list = g_resource['device_list']
    #     for dev_info in dev_list:
    #         if self.__dev_id == dev_info.get('id'):
    #             return dev_info.get('status') == 'free'
    #     return False
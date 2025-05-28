# -*- coding: UTF-8 -*-

"""
File Name:      pc
Author:         zhangwei04
Create Date:    2019/7/11
"""
from selenium import webdriver
from framework.utils.selenium.base_api import BaseApi
from framework.devices.base_device_selenium import BaseDeviceSelenium


class PC(BaseDeviceSelenium, BaseApi):
    """PC 设备对象类，目前适用于Chrome Driver"""
    def __init__(self, target):
        super(PC, self).__init__()
        self.target = target
        self.data = target.data
        self._init_flag = False
        self.driver = webdriver.Chrome()

    def init(self):
        self.driver.maximize_window()
        self._collect_environment()
        self._init_flag = True

    def _collect_environment(self):
        """收集设备信息，并回填到环境字典中"""
        pass

    @property
    def inited(self):
        """
        设备是否初始化标志
        Returns:
            设备是否初始化
        """
        return self._init_flag

    def teardown(self):
        """
        设备类资源释放操作
        """
        self.driver.quit()


__device__ = PC
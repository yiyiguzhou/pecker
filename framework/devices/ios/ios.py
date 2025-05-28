# -*- coding: UTF-8 -*-

"""
File Name:      IOS
Author:         zhangwei04
Create Date:    2018/1/8
"""
import os
from framework.core.resource import g_resource
from framework.devices.base_device_apppium import BaseDeviceAppium
from framework.devices.ios.idevice import IDevice
from framework.logger.logger import g_logger
from framework.devices.ios.device_log import IdeviceSysLog


class IOS(BaseDeviceAppium):
    """
    IOS 设备类
    """
    def __init__(self, target):
        super(IOS, self).__init__(target)
        self.idevice = None

        self.__idevicesyslog = None     # 设备用例idevicesyslog
        self.idev_sys_log_path = None
        self.__log_handle_list = []

    def init(self):
        """设备初始化操作， 包含加载IDevice类、Appium Server"""
        self.use_device()

        self.idevice = IDevice(self.id)

        app_name = self.data.get('app', "")
        if app_name:
            if not app_name.endswith(".ipa"):
                app_name = app_name + ".ipa"
            app_path = os.path.abspath(os.path.join(g_resource['project_path'], 'app_pkg', app_name))
        else:
            app_path = None

        self.desired_caps = {
            'platformName': 'iOS',
            'device': 'iOS',
            'platformVersion': self.idevice.product_version,
            'deviceName': self.idevice.info.get('ProductName', 'iPhone OS'),
            'udid': self.id,
            'desired_capabilities': '',
            'newCommandTimeout': 600,
            'noReset': True,
            'automationName': "XCUITest",
            'app': app_path,
            'bundleId': self.data.get('app_package', "com.iqiyi.iphone"),
        }

        super(IOS, self).init()
        self.__start_dev_log()
        self.__init_flag = True

    def teardown(self):
        """
        IOS设备析构操作
        """
        self.__stop_dev_log()
        super(IOS, self).teardown()

    def __start_dev_log(self):
        """
        开启抓取设备日志,此接口是针对设备生命周期的log抓取
        """
        log_dir = g_resource['log_path']
        if g_resource['testcase_loop'] == 0:
            dev_log_name = "{}_idevicesys_log.txt".format(self.target.name)
        else:
            dev_log_name = "{}_idevicesys_loop{}_log.txt".format(self.target.name, g_resource['testcase_loop'])
        self.idev_sys_log_path = os.path.join(log_dir, dev_log_name)
        idevicesyslog = IdeviceSysLog(dev_id=self.id)
        idevicesyslog.start(self.idev_sys_log_path)
        self.__log_handle_list.append(idevicesyslog)

        super(IOS, self)._start_dev_log()

    def __stop_dev_log(self):
        """
        停止设备日志抓取
        """
        for log_handle in self.__log_handle_list:
            log_handle.stop()

        super(IOS, self)._stop_dev_log()

    def start_log(self):
        """开启用例日志"""
        self.start_idevices_sys_log()

    def stop_log(self):
        """关闭用例日志"""
        self.stop_idevices_sys_log()

    def start_idevices_sys_log(self):
        """
        开启用例设备系统日志
        """
        self.stop_idevices_sys_log()

        idev_sys_log_path = os.path.join(g_resource['testcase_log_dir'],
                                         "{}_{}_idevice_log.txt".format(self.target.name, self.id))
        self.__idevicesyslog = IdeviceSysLog(dev_id=self.id)
        self.__idevicesyslog.start(idev_sys_log_path)

    def stop_idevices_sys_log(self):
        """
        停止用例设备系统日志
        """
        if self.__idevicesyslog:
            self.__idevicesyslog.stop()
            self.__idevicesyslog = None

    def _collect_environment(self):
        """收集环境信息，用于回填到汇总表中"""
        envir_dict = g_resource['aml_data']['environment']
        envir_dict['设备名'] = self.idevice.info.get("ProductName", "")
        envir_dict['设备类型'] = self.idevice.info.get("ProductType", "")
        envir_dict['设备版本号'] = self.idevice.info.get("ProductVersion", "")


__device__ = IOS

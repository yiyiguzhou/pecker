# -*- coding: UTF-8 -*-

"""
File Name:      Android
Author:         zhangwei04
Create Date:    2018/1/8
"""
import os
import re
from framework.core.resource import g_resource
from framework.devices.base_device_apppium import BaseDeviceAppium
from framework.logger.logger import g_logger, g_framework_logger
from framework.devices.android.adb import Adb
from framework.exception.exception import DeviceNotFound
from framework.devices.android.device_log import Logcat
from framework.devices.android.performance import Performance


class Android(BaseDeviceAppium):
    """
    Android设备类
    """

    def __init__(self, target):
        super(Android, self).__init__(target)
        self.adb = None

        self.__logcat = None    # 设备用例logcat handle
        self.logcat_log_path = None
        self.__log_handle_list = []
        self.__performance_handle = None
        self.__msg = {} # 手机信息：如厂商，版本号等

    def init(self):
        """
        初始化设备，包含启动appium server，加载adb通讯类
        """
        self.use_device()
        self.adb = Adb(self.id)
        # 记录当前输入法


        release_ver = self.adb.get_release_version()

        app_name = self.data.get('app', "")
        if app_name:
            if not app_name.endswith("apk"):
                app_name = app_name + ".apk"
            app_path = os.path.abspath(os.path.join(g_resource['project_path'], 'app_pkg', app_name))
        else:
            app_path= None
        unicode_keyboard = self.data.get('unicode_keyboard', True)
        if unicode_keyboard is None:
            unicode_keyboard = True
        elif unicode_keyboard == 'True':
            unicode_keyboard = True
        else:
            unicode_keyboard = False
        self.desired_caps = {
            'platformName': 'Android',
            'platformVersion': release_ver if release_ver else '19',
            'deviceName': 'android',
            'app': app_path,
            'appPackage': self.data.get('app_package', None),  # Ĭ���ǻ��ߵ�app
            'appActivity': self.data.get('app_activity', None),
            'udid': self.id,
            'desired_capabilities': '',
            'newCommandTimeout': 600,
            'noReset': True,
            'unicodeKeyboard': unicode_keyboard,
            'resetKeyboard': True,
            # 'automationName': 'uiautomator2',
        }
        g_framework_logger.info(self.desired_caps)

        super(Android, self).init()
        # 开始抓取设备日志
        self.__start_dev_log()

        # 开始性能数据捕获
        if self.data.get("catch_performance", "").lower() == "true":
            self.__start_performance_catch()
        g_framework_logger.info("adb 启用Unicode输入法")
        self.adb.adb_shell("ime set io.appium.android.ime/.UnicodeIME")
        self.adb.adb_shell("ime enable io.appium.android.ime/.UnicodeIME")
        self._init_flag = True

    def teardown(self):
        """
        Android设备析构操作
        """
        # 恢复输入法
        self.__stop_dev_log()
        self.__stop_performance_catch()

        super(Android, self).teardown()

    def __start_dev_log(self):
        """
        开启抓取设备日志
        """
        log_dir = g_resource['log_path']
        # 开启logcat日志
        self.logcat_log_path = os.path.join(log_dir, "{}_{}_logcat_log.txt".format(self.target.name, self.id))
        logcat = Logcat(adb=self.adb, dev_id=self.id)
        logcat.start(self.logcat_log_path)
        self.__log_handle_list.append(logcat)

        # kmsg日志待添加
        super(Android, self)._start_dev_log()

    def __start_performance_catch(self):
        """开启新能数据捕获
        """
        log_dir = g_resource['log_path']
        time_interval = self.data.get('performance_time_interval', "")
        time_interval = float(time_interval) if time_interval else 1.0
        app_package = self.data.get("catch_performance_app", "")
        if not app_package:
            g_logger.error("device aml file: params 'catch_performance_app' has not found value ")
            return

        self.__performance_handle = Performance(self)
        self.__performance_handle.start_catch(log_dir, app_package, time_interval)

    def __stop_performance_catch(self):
        """停止性能数据捕获"""
        if self.__performance_handle:
            self.__performance_handle.stop()
            self.__performance_handle = None

    def start_log(self):
        """开启业务模块日志"""
        self.start_logcat()

    def stop_log(self):
        """结束业务日志"""
        self.stop_logcat()

    def start_logcat(self) -> object:
        """
        开启用例logcat日志
        """
        if self.__logcat:
            self.__logcat.stop()
        self.__logcat = Logcat(adb=self.adb, dev_id=self.id)
        if g_resource['testcase_loop'] == 0:
            logcat_file_name = "{}_logcat_log.txt".format(self.target.name)
        else:
            logcat_file_name = "{}_logcat_loop{}_log.txt".format(self.target.name, g_resource['testcase_loop'])
        logcat_log_path = os.path.join(g_resource['testcase_log_dir'], logcat_file_name)
        self.__logcat.start(logcat_log_path)

    def stop_logcat(self):
        """
        停止用例logcat日志
        """
        if self.__logcat:
            self.__logcat.stop()
            self.__logcat = None

    def __stop_dev_log(self):
        """
        停止抓取设备日志
        """
        for log_handle in self.__log_handle_list:
            log_handle.stop()

        super(Android, self)._stop_dev_log()

    def _collect_environment(self):
        """收集设备信息，并回填到环境字典中"""
        envir_dict = g_resource['aml_data']['environment']

        envir_dict['设备'] = self.__get_project_device()
        envir_dict['厂商'] = self.get_manufacturer()
        envir_dict['商标'] = self.__get_brand()
        envir_dict['系统版本'] = self.__get_version_release()

    def __get_project_device(self):
        """产品设备信息"""
        ret_msg_list = self.adb.adb_shell("getprop ro.product.device")
        return ret_msg_list[0] if ret_msg_list else ""

    def get_manufacturer(self):
        """生产商"""
        manufacturer = self.__msg.get("manufacturer", None)
        if manufacturer is None:
            ret_msg_list = self.adb.adb_shell("getprop ro.product.manufacturer")
            manufacturer = ret_msg_list[0] if ret_msg_list else ""
            self.__msg["manufacturer"] = manufacturer.lower()
        return manufacturer

    def __get_brand(self):
        """商标"""
        ret_msg_list = self.adb.adb_shell("getprop ro.product.brand")
        return ret_msg_list[0] if ret_msg_list else ""

    def __get_version_release(self):
        """系统版本"""
        ret_msg_list = self.adb.adb_shell("getprop ro.build.version.release")
        return ret_msg_list[0] if ret_msg_list else ""

    def get_ui_version(self):
        """获取UI版本号"""
        ui_version = self.__msg.get("ui_version", None)
        if ui_version is None:
            mobile_product = self.get_manufacturer()
            if mobile_product == "huawei":
                ret_msg_list = self.adb.adb_shell("getprop ro.build.version.emui")
                if ret_msg_list:
                    ui_version = ret_msg_list[0].split("_")[1]
                else:
                    return ""
            elif mobile_product == "xiaomi":
                ret_msg_list = self.adb.adb_shell("getprop ro.build.version.incremental")
                if ret_msg_list:
                    match = re.findall(r'V(\d.\d.\d)', ret_msg_list[0])
                    if match:
                        ui_version = match[0]

                    else:
                        return ""
            else:
                g_logger.error("{} 手机暂未开发获取UI版本号, 返回空字符串".format(mobile_product))
                return ""
            self.__msg['ui_version'] = ui_version

        return ui_version


__device__ = Android

if __name__ == '__main__':
    # device = Android()
    # device.init()
    # device.teardown()
    pass

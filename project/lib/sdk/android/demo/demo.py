# -*- coding: UTF-8 -*-

"""
File Name:      demo
Author:         zhangwei04
Create Date:    2018/1/9
"""
import time
from framework.logger.logger import g_logger
from project.lib.android import Android


class demo(Android):
    def __init__(self, target):
        super().__init__(target=target)
        self.target = target
        self.data = target.data
        self.device = target.device

    def test(self):
        g_logger.info("Demoapk test")
        for i in range(10):
            g_logger.info("current loop: {}".format(i+1))
            pack = self.device.driver.current_package
            activ = self.device.driver.current_activity
            g_logger.info("{}{}".format(self.device.driver.current_package, self.device.driver.current_activity))
            mirror_installed = self.device.driver.is_app_installed('com.lemonjam.intomirror.iqy')
            print(mirror_installed)
            if mirror_installed:
                self.device.start_activity('com.lemonjam.intomirror.iqy', 'org.cocos2dx.cpp.AppActivity')
                time.sleep(1)
            # adb shell "pm list packages|grep mirror"
            g_logger.info("{}{}".format(self.device.driver.current_package, self.device.driver.current_activity))
            self.device.adb.adb_shell('input keyevent KEYCODE_HOME')
            time.sleep(1)
            self.device.launch_app()
            g_logger.info("{}{}".format(self.device.driver.current_package, self.device.driver.current_activity))


    def ansy_test(self):
        import threading
        t = threading.Thread(target=self.test, args=())
        t.start()

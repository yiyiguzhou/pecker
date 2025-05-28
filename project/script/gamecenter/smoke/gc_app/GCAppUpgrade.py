# -*- coding: UTF-8 -*-

"""
File Name:      GCAppUpgrade
Author:         zhangwei04
Create Date:    2018/11/30
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class GCAppUpgrade(TestsuiteNormal):
    """
    预置条件：游戏有福利和游戏圈, 桌面设置成循环滑动
    """
    def setup(self):
        self.desc = "分发App-版本升级"
        DUT.device.start_log()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.check_gc_update(), "分发App卸载、安装与升级", target=DUT)

    def teardown(self):
        DUT.Common.install_app('com.qiyi.gcapp.apk', uninstall_flag=True)
        DUT.device.stop_log()

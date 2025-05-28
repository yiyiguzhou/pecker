# -*- coding: UTF-8 -*-

"""
File Name:      BaseAskIntoGC
Author:         zhangwei04
Create Date:    2019/1/20
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class BaseAskIntoGC(TestsuiteNormal):
    """
    预置条件：游戏有福利和游戏圈, 桌面设置成循环滑动
    """
    def setup(self):
        self.desc = "基线-导航-游戏中心"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.BasePage.into_ask(), "进入基线导航页", target=DUT)
        assert_true(DUT.BasePage.ask_into_gc(), "导航页进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.check_ui(), "检测游戏中心首页UI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

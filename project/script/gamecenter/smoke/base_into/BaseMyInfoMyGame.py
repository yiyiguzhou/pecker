# -*- coding: UTF-8 -*-

"""
File Name:      BaseMyInfoMyGame
Author:         zhangwei04
Create Date:    2019/1/20
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class BaseMyInfoMyGame(TestsuiteNormal):
    """
    预置条件：游戏有福利和游戏圈, 桌面设置成循环滑动
    """
    def setup(self):
        self.desc = "基线-我的-我的游戏-游戏中心"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.BasePage.into_my(), "进入'我的'页面", target=DUT)
        assert_true(DUT.BasePage.my_into_gc(), "从我的游戏进入游戏中心首页", target=DUT)
        assert_true(DUT.HomePage.check_ui(), "检测游戏中心首页UI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

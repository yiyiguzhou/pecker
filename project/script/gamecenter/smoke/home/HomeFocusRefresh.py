# -*- coding: UTF-8 -*-

"""
File Name:      HomeIntoConfPortURL
Author:         zhangwei04
Create Date:    2018/11/19
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class HomeFocusRefresh(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "首页-焦点图刷新"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.HomePage.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.check_focus_refresh(self.data.title), desc="检测轮播图滑动及标题", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
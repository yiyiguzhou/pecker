# -*- coding: UTF-8 -*-

"""
File Name:      HomeIntoConfPortURL
Author:         zhangwei04
Create Date:    2018/11/19
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class HomeSealingTestUI(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "首页-封测专区模块UI检测"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.HomePage.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.check_sealing_test_game_list(self.data.title, self.data.game_num), desc="滑动到封测专区并检测UI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
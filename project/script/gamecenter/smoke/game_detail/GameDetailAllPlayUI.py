# -*- coding: UTF-8 -*-

"""
File Name:      GameDetailAllPlayUI
Author:         zhangwei04
Create Date:    2018/11/30
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class GameDetailAllPlayUI(TestsuiteNormal):
    """
    预置条件：游戏有福利和游戏圈
    """
    def setup(self):
        self.desc = "游戏详情-详情-大家还在玩"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info(self.data.game_name)
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.swipe_down_into_game_detail(self.data.game_name), "进入详情页有福利和游戏圈的游戏", target=DUT)
        assert_true(DUT.GameDetailPage.check_ui(self.data.game_name), "检测详情页UI", target=DUT)
        assert_true(DUT.GameDetailPage.check_more_play_game(), "检测大家还在玩模块", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

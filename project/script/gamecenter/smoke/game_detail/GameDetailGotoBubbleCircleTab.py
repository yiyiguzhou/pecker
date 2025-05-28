# -*- coding: UTF-8 -*-

"""
File Name:      GameDetailGotoBubbleCircleTab
Author:         zhangwei04
Create Date:    2018/11/30
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class GameDetailGotoBubbleCircleTab(TestsuiteNormal):
    """
    预置条件：游戏有福利和游戏圈
    """
    def setup(self):
        self.desc = "游戏详情-详情-游戏圈"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("游戏名: {}".format(self.data.game_name))
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.swipe_down_into_game_detail(self.data.game_name), "进入详情页有福利和游戏圈的游戏", target=DUT)
        assert_true(DUT.GameDetailPage.check_ui(self.data.game_name), "检测详情页UI", target=DUT)
        assert_true(DUT.GameDetailPage.detail_goto_more_bubble_circle(), "进入更多游戏圈", target=DUT)
        assert_true(DUT.GameDetailPage.check_bubble_circle_tab(), "检测游戏圈TabUI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

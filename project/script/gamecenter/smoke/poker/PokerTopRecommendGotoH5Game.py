# -*- coding: UTF-8 -*-

"""
File Name:      PokerTopRecommendGotoH5Game
Author:         zhangwei04
Create Date:    2018/12/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class PokerTopRecommendGotoH5Game(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "棋牌-顶部推荐-免下载畅玩入口"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.into_poker(), "进入棋牌中心", target=DUT)
        assert_true(DUT.PokerPage.check_ui(), "棋牌中心检测UI", target=DUT)
        assert_true(DUT.PokerPage.check_top_recommend_play_without_dl(), "免下载畅玩入口", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

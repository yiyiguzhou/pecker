# -*- coding: UTF-8 -*-

"""
File Name:      RankUI
Author:         gufangmei_sx
Create Date:    2018/8/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class RankUI(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "排行榜UI"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.goto_rank(), "进入榜单页", target=DUT)
        assert_true(DUT.RankPage.check_ui(), "榜单页检测UI", target=DUT)
        assert_true(DUT.RankPage.check_tab_top_game(self.data.game_name), "检测默认页(精品榜)游戏列表", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
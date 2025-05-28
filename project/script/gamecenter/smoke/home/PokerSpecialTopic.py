# -*- coding: UTF-8 -*-

"""
File Name:      PokerSpecialTopic
Author:         gufangmei_sx
Create Date:    2018/7/11
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class PokerSpecialTopic(TestsuiteNormal):
    """
    用例描述：首页-子业务入口-棋牌入口
    预置条件：
    """
    def setup(self):
        self.desc = "首页-子业务入口-棋牌入口"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.into_poker(self.data.special_topic), "进入棋牌专题页", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
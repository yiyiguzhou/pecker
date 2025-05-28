# -*- coding: UTF-8 -*-

"""
File Name:      GameDetailsPageUI
Author:         gufangmei_sx
Create Date:    2018/8/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class GameDetailsPageUI(TestsuiteNormal):
    """
    用例描述：游戏详情页-UI及顶部栏
    预置条件：游戏同时存在详情、福利、圈子三个tab，且游戏配置了背景图
    """
    def setup(self):
        self.desc = "游戏详情页-UI及顶部栏"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("游戏同时存在详情、福利、游戏圈三个tab，且游戏配置了背景图")
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.swipe_down_into_game_detail(self.data.game_name), "向下滑动寻找{}游戏进入游戏详情".format(self.data.game_name), target=DUT)
        assert_true(DUT.GameDetailPage.check_ui(self.data.game_name), "游戏详情页检测UI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
# -*- coding: UTF-8 -*-

"""
File Name:      PokerHorizontalGame
Author:         zhangwei04
Create Date:    2018/12/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class PokerHorizontalGame(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "棋牌-横排游戏-安装&显示"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.into_poker(), "进入棋牌中心", target=DUT)
        assert_true(DUT.PokerPage.check_ui(), "棋牌中心检测UI", target=DUT)
        assert_true(DUT.PokerPage.horizontal_into_game_detail(self.data.title, self.data.game_title), "横排进入游戏详情页", target=DUT)
        assert_true(DUT.GameDetailPage.check_ui(self.data.game_name), "游戏详情页检测UI", target=DUT)
        # assert_true(DUT.GameDetailPage.game_download_and_install(self.data.game_name, open_game=False), "下载、安装游戏", target=DUT)
        # assert_true(DUT.GameDetailPage.uninstall_game(self.data.game_name), "卸载游戏", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

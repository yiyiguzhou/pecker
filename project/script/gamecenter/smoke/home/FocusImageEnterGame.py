# -*- coding: UTF-8 -*-

"""
File Name:      FocusImageEnterGame
Author:         gufangmei_sx
Create Date:    2018/7/9
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class FocusImageEnterGame(TestsuiteNormal):
    """
    用例描述：首页-焦点图进入游戏详情页
    预置条件：1. 奇玩1.0后台运营位：1339配置一张焦点图，且该焦点图配置进入游戏详情页。
    """
    def setup(self):
        self.desc = "首页-焦点图进入游戏详情页"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.Recommend.into_focus_detail_page(self.data.game_title), "点击焦点图进入详情页", target=DUT)
        assert_true(DUT.GameDetailPage.check_ui(self.data.game_name), "查看详情信息", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
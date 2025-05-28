# -*- coding: UTF-8 -*-

"""
File Name:      GameList
Author:         gufangmei_sx
Create Date:    2018/7/10
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class GameList(TestsuiteNormal):
    """
    用例描述：首页-游戏列表模板运营位
    预置条件：1. 奇玩1.0后台运营位：1372配置了游戏列表模板运营位一的标题；运营位：1380配置了8款游戏。
    """
    def setup(self):
        self.desc = "首页-游戏列表模板运营位"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.Common.check_title(self.data.title, timeout=300), "游戏列表 ", target=DUT)
        assert_true(DUT.HomePage.game_list_look_all(self.data.title, self.data.special_topic), "全部游戏列表", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
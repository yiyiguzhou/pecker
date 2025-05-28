# -*- coding: UTF-8 -*-

"""
File Name:      ListPageSoaring
Author:         gufangmei_sx
Create Date:    2018/8/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class ListPageSoaring(TestsuiteNormal):
    """
    用例描述：榜单页-飙升榜tab
    预置条件：运营位：1471配置了三款游戏。
    """
    def setup(self):
        self.desc = "榜单页-飙升榜tab"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("运营位：1471配置了三款游戏。")
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.game_center_into_list_page(), "进入榜单页", target=DUT)
        assert_true(DUT.Common.click_title(self.data.title), "进入飙升榜tab", target=DUT)
        assert_true(DUT.HomePage.check_game_order(self.data.game), "检查多款游戏的顺序", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
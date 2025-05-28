# -*- coding: UTF-8 -*-

"""
File Name:      NewGameSealTab
Author:         gufangmei_sx
Create Date:    2018/8/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class NewGameSealTab(TestsuiteNormal):
    """
    用例描述：新游页-封测专区tab
    预置条件：运营位：923配置了两款游戏。
    """
    def setup(self):
        self.desc = "新游页-封测专区tab"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("运营位：923配置了两款游戏。")
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.into_new_game(), "进入新游", target=DUT)
        assert_true(DUT.Common.click_and_check(self.data.seal_tab, self.data.title), "进入封测专区tab", target=DUT)
        assert_true(DUT.HomePage.check_sealing_game(self.data.game), "检查游戏", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
# -*- coding: UTF-8 -*-

"""
File Name:      NewGameReservationTab
Author:         gufangmei_sx
Create Date:    2018/8/10
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class NewGameReservationTab(TestsuiteNormal):
    """
    用例描述：新游页-新游预约tab
    预置条件：运营位：1487配置了3款新游预约tab的置顶游戏。
    """
    def setup(self):
        self.desc = "新游页-新游预约tab"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("运营位：1487配置了3款新游预约tab的置顶游戏。")
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.into_new_game(), "进入新游", target=DUT)
        assert_true(DUT.Common.click_and_check(self.data.reservation_tab, self.data.title), "进入最新预约tab", target=DUT)
        assert_true(DUT.HomePage.check_latest_reservation(self.data.game1, self.data.game2, self.data.game3), "检查上方三个游戏", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
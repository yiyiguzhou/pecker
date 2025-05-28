# -*- coding: UTF-8 -*-

"""
File Name:      HomeIntoConfPortURL
Author:         zhangwei04
Create Date:    2018/11/19
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class HomeReservationIntoReservationTab(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "首页-预约模板更多-新游预约Tab"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.HomePage.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.reservation_look_more(), desc="预约模块点击更多进入H5活动页", target=DUT)
        assert_true(DUT.NewGamePage.check_ui(), desc='检查新游页UI', target=DUT)

    def teardown(self):
        DUT.device.stop_log()

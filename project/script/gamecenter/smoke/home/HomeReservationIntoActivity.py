# -*- coding: UTF-8 -*-

"""
File Name:      HomeIntoConfPortURL
Author:         zhangwei04
Create Date:    2018/11/19
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class HomeReservationIntoActivity(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "首页-预约模块-H5活动页"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info(self.data.game_name)
        assert_true(DUT.HomePage.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.reservation_into(self.data.game_name), desc="预约模块进入H5活动页", target=DUT)
        assert_true(DUT.H5Page.check_ui(), desc='检查H5活动页', target=DUT)

    def teardown(self):
        DUT.device.stop_log()
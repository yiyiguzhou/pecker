# -*- coding: UTF-8 -*-

"""
File Name:      HomeBottomConfPortUI
Author:         gufangmei_sx
Create Date:    2018/8/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class HomeBottomConfPortUI(TestsuiteNormal):
    """
    预置条件：底部栏配置入口
    """
    def setup(self):
        self.desc = "首页-底部栏可配置入口UI"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.check_home_bottom_ui(self.data.title), "底部栏检测", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
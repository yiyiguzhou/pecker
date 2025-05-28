# -*- coding: UTF-8 -*-

"""
File Name:      MyInforUI
Author:         zhangwei04
Create Date:    2018/1/2
"""
import time
# from project.script.testsuite.TestsuiteNormal import *
from project.script.gamecenter.testsuite.TestsuiteMyInfo import *


class MyInforUI(TestsuiteMyInfo):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "个人中心UI"
        DUT.device.start_log()
        # DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        # assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.Common.back_to_homepage())

        assert_true(DUT.HomePage.into_my_info(), "进入个人中心", target=DUT)
        assert_true(DUT.MyInfoPage.check_ui(), "个人中心检测UI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

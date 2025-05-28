# -*- coding: UTF-8 -*-

"""
File Name:      HomeFullScreenGotoGD
Author:         zhangwei04
Create Date:    2018/11/19
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class HomeFullScreenGotoGD(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "首页-全屏弹窗-游戏详情页"
        DUT.device.start_log()
        DUT.Common.clear_app_data(launch_app=True)

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.HomePage.into_game_center_without_check(), "进入游戏中心,不检测UI", target=DUT)
        assert_true(DUT.HomePage.full_screen_goto_game_detail(), desc="全屏弹窗进入游戏详情页", target=DUT)
        assert_true(DUT.GameDetailPage.check_ui(game_name=self.data.game_name), desc="游戏详情页检测UI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
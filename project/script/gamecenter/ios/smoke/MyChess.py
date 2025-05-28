# -*- coding: UTF-8 -*-

"""
File Name:      MyChess
Author:         gufangmei_sx
Create Date:    2018/8/22
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class MyChess(TestsuiteNormal):

    def setup(self):
        DUT.device.start_log()
        DUT.Smoke.reset_app()

    def test(self):

        g_logger.info("游戏中心已登录")
        time.sleep(15)
        assert_true(DUT.Smoke.into_ios_game_center(), "进入游戏中心", target=DUT)
        assert_true(DUT.Smoke.enter_my_chess_area(), "进入我的棋牌专区", target=DUT)
        assert_true(DUT.Smoke.check_event_title(self.data.game), "检查活动文字", target=DUT)
        assert_true(DUT.Smoke.click_and_check_gamedetail(), "检查棋牌游戏详情", target=DUT)
        assert_true(DUT.Smoke.click_and_check_game_appstore(), "检查是否正确进入appstore", target=DUT)
        time.sleep(3)

    def teardown(self):
        DUT.device.stop_log()

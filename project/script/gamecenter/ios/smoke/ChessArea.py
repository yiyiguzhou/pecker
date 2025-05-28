# -*- coding: UTF-8 -*-

"""
File Name:      ChessArea
Author:         gufangmei_sx
Create Date:    2018/8/1
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class ChessArea(TestsuiteNormal):

    def setup(self):
        DUT.device.start_log()
        DUT.Smoke.reset_app()

    def test(self):

        assert_true(DUT.Smoke.into_ios_game_center(), "进入游戏中心", target=DUT)
        assert_true(DUT.Smoke.click_chess_area(), "进入主页棋牌专区", target=DUT)
        assert_true(DUT.Smoke.check_event_title(self.data.title), "检查活动文字", target=DUT)
        assert_true(DUT.Smoke.chess_area_back(), "返回推荐页面", target=DUT)
        assert_true(DUT.Smoke.enter_my_chess_area(), "进入我的棋牌专区", target=DUT)
        assert_true(DUT.Smoke.check_event_title(self.data.title), "检查活动文字", target=DUT)
        time.sleep(3)

    def teardown(self):
        DUT.device.stop_log()

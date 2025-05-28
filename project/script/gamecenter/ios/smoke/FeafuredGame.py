# -*- coding: UTF-8 -*-

"""
File Name:      FeafuredGame
Author:         gufangmei_sx
Create Date:    2018/9/18
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class FeafuredGame(TestsuiteNormal):
    """
        用例描述：我的页-为您精选
        预置条件：
    """
    def setup(self):
        DUT.device.start_log()
        DUT.Smoke.reset_app()

    def test(self):

        assert_true(DUT.Smoke.into_ios_game_center(), "进入游戏中心", target=DUT)
        assert_true(DUT.Smoke.base_my_game(), "进入我的游戏", target=DUT)
        assert_true(DUT.Smoke.check_event_title(self.data.title), "检查活动文字", target=DUT)
        assert_true(DUT.Smoke.check_game_name(self.data.game1, self.data.game2, self.data.game3, self.data.game4), "检查为您精选游戏", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

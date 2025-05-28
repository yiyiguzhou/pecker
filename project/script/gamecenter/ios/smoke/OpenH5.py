# -*- coding: UTF-8 -*-

"""
File Name:      OpenH5
Author:         gufangmei_sx
Create Date:    2018/9/17
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class OpenH5(TestsuiteNormal):

    def setup(self):
        DUT.device.start_log()
        DUT.Smoke.reset_app()

    def test(self):
        assert_true(DUT.Smoke.into_ios_game_center(), "进入游戏中心", target=DUT)
        assert_true(DUT.Smoke.base_my_game(), "进入我的游戏", target=DUT)
        assert_true(DUT.Smoke.click_and_play(self.data.UID), "点击点击即玩", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

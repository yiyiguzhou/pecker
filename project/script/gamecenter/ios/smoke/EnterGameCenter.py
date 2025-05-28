# -*- coding: UTF-8 -*-

"""
File Name:      EnterGameCenter
Author:         gufangmei_sx
Create Date:    2018/7/27
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class EnterGameCenter(TestsuiteNormal):
    """
    用例描述：进入游戏中心
    预置条件：
    """
    def setup(self):
        DUT.device.start_log()
        DUT.Smoke.reset_app()

    def test(self):
        assert_true(DUT.Smoke.into_ios_game_center(), "进入游戏中心", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

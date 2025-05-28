# -*- coding: UTF-8 -*-

"""
File Name:      SmallTopic
Author:         gufangmei_sx
Create Date:    2018/9/4
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class SmallTopic(TestsuiteNormal):
    """
    用例描述：点击小专题
    预置条件：运营位已配置(配置3个）
    """
    def setup(self):
        DUT.device.start_log()
        DUT.Smoke.reset_app()

    def test(self):
        assert_true(DUT.Smoke.into_ios_game_center(), "进入游戏中心", target=DUT)


    def teardown(self):
        DUT.device.stop_log()

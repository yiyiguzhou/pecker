# -*- coding: UTF-8 -*-

"""
File Name:      GameReservation
Author:         gufangmei_sx
Create Date:    2018/9/4
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class GameReservation(TestsuiteNormal):
    """
    用例描述：点击“预约”跳转
    预置条件：
    """
    def setup(self):
        DUT.device.start_log()
        DUT.Smoke.reset_app()

    def test(self):
        assert_true(DUT.Smoke.into_ios_game_center(), "进入游戏中心", target=DUT)
        assert_true(DUT.Smoke.click_button("'//Users//wzhang//doc//svn//auto//code//ipecker//project//conf//img//4.png'"), "点击预约按钮", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

# -*- coding: UTF-8 -*-

"""
File Name:      SignIn
Author:         gufangmei_sx
Create Date:    2018/8/1
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class SignIn(TestsuiteNormal):
    """
    用例描述：签到
    预置条件：用户已登录
    """
    def setup(self):
        DUT.device.start_log()
        DUT.Smoke.reset_app()

    def test(self):

        # assert_true(DUT.Smoke.into_ios_game_center(), "进入游戏中心", target=DUT)
        assert_true(DUT.Smoke.click_sign_in(self.data.account, self.data.password), "签到", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
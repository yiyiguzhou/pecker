# -*- coding: UTF-8 -*-

"""
File Name:      LoginIn
Author:         gufangmei_sx
Create Date:    2018/7/31
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class LoginIn(TestsuiteNormal):
    """
        用例描述：密码登录
        预置条件：用户未登录
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Smoke.reset_app()

    def test(self):
        assert_true(DUT.Smoke.logout(), "退出登录", target=DUT)
        assert_true(DUT.Smoke.into_ios_game_center(), "进入游戏中心", target=DUT)
        assert_true(DUT.Smoke.base_my_game(), "进入我的游戏", target=DUT)
        assert_true(DUT.Smoke.login_in(self.data.account, self.data.password), "密码登录", target=DUT)
        assert_true(DUT.Smoke.check_title(self.data.title), "检查用户信息", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
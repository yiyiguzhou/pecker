# -*- coding: UTF-8 -*-

"""
File Name:      PasswordLogin
Author:         gufangmei_sx
Create Date:    2018/8/8
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class PasswordLogin(TestsuiteNormal):
    """
    用例描述：登录-个人中心-密码登录
    预置条件：用户处于未登录状态。
    """
    def setup(self):
        self.desc = "登录-个人中心-密码登录"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Login.base_login_out(), "退出登录", target=DUT)
        g_logger.info("用户处于未登录状态")
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.Login.into_login_page(), "进入游戏中心登录页面", target=DUT)
        assert_true(DUT.Login.login_in_with_password(self.data.account, self.data.password), "密码登录", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
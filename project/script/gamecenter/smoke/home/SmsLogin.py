# -*- coding: UTF-8 -*-

"""
File Name:      SmsLogin
Author:         gufangmei_sx
Create Date:    2018/8/8
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class SmsLogin(TestsuiteNormal):
    """
    用例描述：游戏中心-个人中心-短信登录
    预置条件：用户处于未登录状态
    """
    def setup(self):
        self.desc = "游戏中心-个人中心-短信登录"
        DUT.device.start_log()
        DUT.Common.start_ipecker_app()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Login.base_login_out(), "退出登录", target=DUT)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.Login.into_login_page(), "从个人中心进入登录页面", target=DUT)
        assert_true(DUT.Login.login_in_with_sms(self.data.account), "短信登录", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

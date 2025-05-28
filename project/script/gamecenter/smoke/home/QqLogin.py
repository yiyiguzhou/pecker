# -*- coding: UTF-8 -*-

"""
File Name:      QqLogin
Author:         gufangmei_sx
Create Date:    2018/8/8
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class QqLogin(TestsuiteNormal):
    """
    用例描述：游戏中心-个人中心-QQ登录
    预置条件：QQ已登录。
    """
    def setup(self):
        self.desc = "游戏中心-个人中心-QQ登录"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Login.base_login_out(), "退出登录", target=DUT)
        g_logger.info("手机已安装qq软件且已登录，爱奇艺用户处于未登录状态")
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        # assert_true(DUT.Login.into_login_page_bought(), "从已购买tab进入基线登录页面", target=DUT)
        assert_true(DUT.Login.into_login_page(), "从个人中心进入登录页面", target=DUT)
        assert_true(DUT.Login.login_in_with_qq(), "qq登录",target=DUT)

    def teardown(self):
        DUT.device.stop_log()
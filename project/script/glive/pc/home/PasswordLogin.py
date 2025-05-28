# -*- coding: UTF-8 -*-

"""
File Name:      PasswordLogin
Author:         zhangwei04
Create Date:    2019/7/19
"""

from project.script.testsuite.TestsuiteNormal import *
import os


class PasswordLogin(TestsuiteNormal):
    def setup(self):
        self.desc = "首页-密码登录"

    def test(self):
        g_logger.info(self.desc)
        DUT.Home.into_home()
        assert_true(DUT.Login.password_login(account_section="user1"), desc="密码登录", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
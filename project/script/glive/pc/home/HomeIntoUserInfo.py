# -*- coding: UTF-8 -*-

"""
File Name:      HomeUserChargeUI
Author:         zhangwei04
Create Date:    2019/7/19
"""

from project.script.testsuite.TestsuiteNormal import *
import os


class HomeIntoUserInfo(TestsuiteNormal):
    def setup(self):
        self.desc = "首页-个人中心-个人信息"

    def test(self):
        DUT.Home.into_home()
        g_logger.info(self.desc)
        assert_true(DUT.Login.password_login(account_section='user1'), desc="密码登录", target=DUT)
        assert_true(DUT.Home.click_user_icon(), desc="点击用户图标", target=DUT)
        assert_true(DUT.UserPage.check_info_ui(account_section='user1'), desc='检测用户个人信息页UI', target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
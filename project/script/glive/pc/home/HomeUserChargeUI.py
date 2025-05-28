# -*- coding: UTF-8 -*-

"""
File Name:      HomeUserChargeUI
Author:         zhangwei04
Create Date:    2019/7/19
"""

from project.script.testsuite.TestsuiteNormal import *
import os


class HomeUserChargeUI(TestsuiteNormal):
    def setup(self):
        self.desc = "首页-个人信息-充值-页面检测"

    def test(self):
        DUT.Home.into_home()
        g_logger.info(self.desc)
        assert_true(DUT.Login.password_login(account_section='user1'), desc="密码登录", target=DUT)
        assert_true(DUT.Home.click_charge_button(), desc="点击充值按钮", target=DUT)
        assert_true(DUT.Home.check_charge_ui(), desc='检测充值界面UI', target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
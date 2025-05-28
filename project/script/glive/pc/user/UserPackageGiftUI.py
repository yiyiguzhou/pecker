# -*- coding: UTF-8 -*-

"""
File Name:      UserPackageGiftUI
Author:         zhangwei04
Create Date:    2019/7/26
"""

from project.script.testsuite.TestsuiteNormal import *
import os


class UserPackageGiftUI(TestsuiteNormal):
    def setup(self):
        self.desc = "个人中心-背包-礼物UI"

    def test(self):
        DUT.Home.into_home()
        g_logger.info(self.desc)
        assert_true(DUT.Login.password_login(account_section='user1'), desc="密码登录", target=DUT)
        assert_true(DUT.Home.into_user_center(), desc="进入个人中心", target=DUT)
        assert_true(DUT.UserPage.click_tab("我的背包"), desc='进入我的背包Tab', target=DUT)
        assert_true(DUT.UserPage.check_package_gift_ui(), desc='检测我的背包礼物道具页面', target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
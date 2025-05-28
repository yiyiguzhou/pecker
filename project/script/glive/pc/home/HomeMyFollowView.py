# -*- coding: UTF-8 -*-

"""
File Name:      HomeMyFollowView
Author:         zhangwei04
Create Date:    2019/7/24
"""

from project.script.testsuite.TestsuiteNormal import *
import os


class HomeMyFollowView(TestsuiteNormal):
    def setup(self):
        self.desc = "首页-我的关注-UI检测"

    def test(self):
        DUT.Home.into_home()
        g_logger.info(self.desc)
        assert_true(DUT.Login.password_login(account_section='user1'), desc="密码登录", target=DUT)
        assert_true(DUT.Home.click_follow(), desc="点击我的关注，弹出关注列表弹窗", target=DUT)
        assert_true(DUT.Home.check_follow_scroll(), desc="检测关注列表弹窗", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
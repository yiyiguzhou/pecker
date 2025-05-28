# -*- coding: UTF-8 -*-

"""
File Name:      PasswordLogin
Author:         zhangwei04
Create Date:    2019/7/19
"""

from project.script.testsuite.TestsuiteNormal import *
import os


class HomeClickLogo(TestsuiteNormal):
    def setup(self):
        self.desc = "首页-点击爱奇艺Logo图标"

    def test(self):
        g_logger.info(self.desc)
        DUT.Home.into_home()
        assert_true(DUT.Home.click_logo(), desc="点击Logo,并检测是否新弹出窗口", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
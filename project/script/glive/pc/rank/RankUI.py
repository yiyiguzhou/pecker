# -*- coding: UTF-8 -*-

"""
File Name:      PasswordLogin
Author:         zhangwei04
Create Date:    2019/7/19
"""

from project.script.testsuite.TestsuiteNormal import *
import os


class RankUI(TestsuiteNormal):
    def setup(self):
        self.desc = "榜单页-UI检测"

    def test(self):
        DUT.Home.into_home()
        g_logger.info(self.desc)
        assert_true(DUT.Home.into_rank(), desc="点击主播排行榜", target=DUT)
        assert_true(DUT.RankPage.check_rank_ui(), desc="检测榜单页UI", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
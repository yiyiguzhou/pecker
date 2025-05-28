# -*- coding: UTF-8 -*-

"""
File Name:      HomeSearch
Author:         zhangwei04
Create Date:    2019/7/23
"""

from project.script.testsuite.TestsuiteNormal import *
import os


class HomeSearch(TestsuiteNormal):
    def setup(self):
        self.desc = "首页-导航栏-搜索"

    def test(self):
        DUT.Home.into_home()
        g_logger.info(self.desc)
        assert_true(DUT.Home.search(self.data.text), desc="输入文本并搜索", target=DUT)
        assert_true(DUT.SearchPage.check_ui(self.data.text), desc="搜索页检测UI", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
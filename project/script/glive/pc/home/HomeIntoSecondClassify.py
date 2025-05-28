# -*- coding: UTF-8 -*-

"""
File Name:      HomeIntoSecondClassify
Author:         zhangwei04
Create Date:    2019/7/23
"""

from project.script.testsuite.TestsuiteNormal import *
import os


class HomeIntoSecondClassify(TestsuiteNormal):
    def setup(self):
        self.desc = "首页-二级分类标签"

    def test(self):
        DUT.Home.into_home()
        g_logger.info(self.desc)
        assert_true(DUT.Home.into_second_classify(self.data.subtitle), desc="进入子标题[{}]页".format(self.data.subtitle), target=DUT)
        assert_true(DUT.LiveListPage.check_ui(self.data.title, active=self.data.subtitle, tabs=self.data.tabs), desc="检测列表页UI", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
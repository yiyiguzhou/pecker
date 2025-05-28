# -*- coding: UTF-8 -*-

"""
File Name:      PasswordLogin
Author:         zhangwei04
Create Date:    2019/7/19
"""

from project.script.testsuite.TestsuiteNormal import *
import os


class HomeSideListSwitch(TestsuiteNormal):
    def setup(self):
        self.desc = "首页-列表页-切换"

    def test(self):
        DUT.Home.into_home()
        g_logger.info(self.desc)
        for title in self.data.title:
            assert_true(DUT.Home.into_side_list_title(title), desc="查找导航列表，点击标题{}".format(title), target=DUT)
            assert_true(DUT.Home.check_subtitle_page(title), desc="检测跳转后的标题页", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
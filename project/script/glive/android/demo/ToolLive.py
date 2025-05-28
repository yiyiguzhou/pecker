# -*- coding: UTF-8 -*-

"""
File Name:      ToolLogin
Author:         zhangwei04
Create Date:    2019/7/12
"""


from project.script.testsuite.TestsuiteNormal import *
import os


class ToolLive(TestsuiteNormal):
    def setup(self):
        pass

    def test(self):
        account_section = "anchor1"
        assert_true(DUT.LiveTool.once_step_live(account_section, self.data.title, self.data.second_lab), "直播工具开播")
        assert_true(DUT.LiveTool.stop_live(), "关闭直播")

    def teardown(self):
        pass
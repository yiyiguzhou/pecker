# -*- coding: UTF-8 -*-

"""
File Name:      HomeIntoConfPortURL
Author:         zhangwei04
Create Date:    2018/11/19
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class HomeSearchDefaultText(TestsuiteNormal):
    """
    用例描述：首页-搜索-默认搜索词
    预置条件：无
    """
    def setup(self):
        self.desc = "首页-搜索-默认搜索词"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.HomePage.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.check_search_default_text(self.data.defalut_text), "检测搜索栏默认搜索词", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
# -*- coding: UTF-8 -*-

"""
File Name:      TopSearch
Author:         gufangmei_sx
Create Date:    2018/7/6
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class TopSearch(TestsuiteNormal):
    """
    用例描述：首页-顶部栏搜索按钮
    预置条件：
    """
    def setup(self):
        self.desc = "首页-顶部栏搜索按钮"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.game_center_search(self.data.search_text), "搜索成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
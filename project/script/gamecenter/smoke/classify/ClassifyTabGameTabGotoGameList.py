# -*- coding: UTF-8 -*-

"""
File Name:      ClassifyTabGameTabGotoGameList
Author:         zhangwei04
Create Date:    2018/12/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class ClassifyTabGameTabGotoGameList(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "分类-类别标签页-游戏标签-游戏列表"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("检测标签：{}".format(self.data.tab_name))
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.goto_classify(), "进入分类页", target=DUT)
        assert_true(DUT.ClassifyPage.click_tab(self.data.tab_name), "点击标签", target=DUT)
        assert_true(DUT.ClassifyPage.click_game_tags(self.data.tags_name), "点击游戏分类页标签", target=DUT)
        assert_true(DUT.ClassifyPage.check_game_list_page(self.data.tags_name, self.data.game_name), "检测游戏列表页", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

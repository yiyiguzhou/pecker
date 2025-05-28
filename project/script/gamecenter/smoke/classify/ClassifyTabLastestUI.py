# -*- coding: UTF-8 -*-

"""
File Name:      ClassifyTabLastestUI
Author:         zhangwei04
Create Date:    2018/12/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class ClassifyTabLastestUI(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "分类-类别标签页-最新排行"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("检测标签：{}".format(self.data.tab_name))
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.goto_classify(), "进入分类页", target=DUT)
        assert_true(DUT.ClassifyPage.click_tab(self.data.tab_name), "点击标签", target=DUT)
        assert_true(DUT.ClassifyPage.tab_switch_lastest_icon(), "切换至最新标签页", target=DUT)
        assert_true(DUT.ClassifyPage.check_tab_lastest_ui(self.data.tab_name, game_name=self.data.game_name), "检测默认处于最热标签页", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

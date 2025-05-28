# -*- coding: UTF-8 -*-

"""
File Name:      NewGameLatestBookNumber
Author:         gufangmei_sx
Create Date:    2018/8/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class NewGameLatestBookNumber(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "新游-最新预约-人数"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.into_new_game(), "进入新游页", target=DUT)
        time.sleep(3)   # 等待3秒页面加载稳定
        assert_true(DUT.NewGamePage.click_latest_book_tab(), "点击最新预约标签", target=DUT)
        assert_true(DUT.NewGamePage.check_book_tab_ui(), "检测最新预约页面 UI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
# -*- coding: UTF-8 -*-

"""
File Name:      HomeIntoConfPortURL
Author:         zhangwei04
Create Date:    2018/11/19
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class HomeSearchText(TestsuiteNormal):
    """
    预置条件：无
    点击游戏列表的游戏，根据游戏游戏icon进入游戏详情页
    """
    def setup(self):
        self.desc = "首页-搜索-带联想词搜索"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.HomePage.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        time.sleep(5)  # 等待搜索框加载稳定
        assert_true(DUT.HomePage.game_search_click_icon(self.data.game_name), "搜索游戏：{}".format(self.data.game_name), target=DUT)
        assert_true(DUT.GameDetailPage.check_ui(self.data.game_name, click_tab=False), desc="检测游戏详情页UI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
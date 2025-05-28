# -*- coding: UTF-8 -*-

"""
File Name:      GameDetailWelfareGotoAcitvityPage
Author:         zhangwei04
Create Date:    2018/11/30
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class GameDetailWelfareGotoAcitvityPage(TestsuiteNormal):
    """
    预置条件：游戏有福利和游戏圈
    """
    def setup(self):
        self.desc = "游戏详情-福利-专项活动"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.swipe_down_into_game_detail(self.data.game_name), "进入详情页有福利和游戏圈的游戏", target=DUT)
        assert_true(DUT.GameDetailPage.check_ui(self.data.game_name), "检测详情页UI", target=DUT)
        assert_true(DUT.GameDetailPage.detail_goto_all_welfare(), "点击全部福利进入福利Tab页", target=DUT)
        assert_true(DUT.GameDetailPage.welfare_goto_fisrt_activity(), "进入第一个专属活动", target=DUT)
        assert_true(DUT.H5Page.check_ui(), "确认是否进入专属活动页", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

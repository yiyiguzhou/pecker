# -*- coding: UTF-8 -*-

"""
File Name:      GameDetailWelfareUI
Author:         zhangwei04
Create Date:    2018/11/30
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class GameDetailWelfareUI(TestsuiteNormal):
    """
    预置条件：游戏有福利和游戏圈
    """
    def setup(self):
        self.desc = "游戏详情-福利UI"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("进入游戏详情页-福利tab，查看启动特权、代金券、专享活动、专享礼包、激活码礼包是否正确显示（没有则不显示），点击有码礼包是否能够进入礼包详情页")
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.swipe_down_into_game_detail(self.data.game_name), "进入详情页有福利和游戏圈的游戏", target=DUT)
        assert_true(DUT.GameDetailPage.check_ui(self.data.game_name), "检测详情页UI", target=DUT)
        assert_true(DUT.GameDetailPage.into_welfare_tab(), "进入福利Tab", target=DUT)
        assert_true(DUT.GameDetailPage.check_welfare_ui(), "检测福利TabUI", target=DUT)
        assert_true(DUT.GameDetailPage.welfare_into_gift_detail(), "福利Tab进入礼包详情页", target=DUT)
        assert_true(DUT.GameDetailPage.check_gift_detail_ui(), "检测礼包详情页UI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

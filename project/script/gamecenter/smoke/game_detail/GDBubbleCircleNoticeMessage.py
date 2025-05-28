# -*- coding: UTF-8 -*-

"""
File Name:      GDBubbleCircleNoticeMessage
Author:         zhangwei04
Create Date:    2018/11/30
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class GDBubbleCircleNoticeMessage(TestsuiteNormal):
    """
    预置条件：游戏有福利和游戏圈
    """
    def setup(self):
        self.desc = "游戏详情-游戏圈-公告|泡泡消息"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.swipe_down_into_game_detail(self.data.game_name), "进入详情页有福利和游戏圈的游戏", target=DUT)
        assert_true(DUT.GameDetailPage.into_bubble_circle_tab(), "点击游戏圈Tab", target=DUT)
        assert_true(DUT.GameDetailPage.bubble_circle_into_notice(), "若有公告，进入公告详情页", target=DUT)
        assert_true(DUT.GameDetailPage.bubble_circle_into_message(), "进入发布消息详情页", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

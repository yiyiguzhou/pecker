# -*- coding: UTF-8 -*-

"""
File Name:      GDBubbleCircleVideoFollow
Author:         zhangwei04
Create Date:    2018/11/30
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class GDBubbleCircleVideoFollow(TestsuiteNormal):
    """
    预置条件：游戏详情页有福利和游戏圈
    """
    def setup(self):
        self.desc = "游戏详情-游戏圈-视频转发"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Login.base_login_out(), "退出登录", target=DUT)
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.Login.into_login_page(), "进入游戏中心登录页面", target=DUT)
        assert_true(DUT.Login.login_in_with_password(self.data.account, self.data.password), "密码登录", target=DUT)
        DUT.Common.back_common_title()
        assert_true(DUT.HomePage.swipe_down_into_game_detail(self.data.game_name), "进入详情页有福利和游戏圈的游戏", target=DUT)
        assert_true(DUT.GameDetailPage.into_bubble_circle_tab(), "点击游戏圈Tab", target=DUT)
        assert_true(DUT.GameDetailPage.check_bubble_circle_tab(), "检测游戏圈TabUI", target=DUT)
        assert_true(DUT.GameDetailPage.bubble_circle_video_follow(self.data.comment), "游戏圈转发视频", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

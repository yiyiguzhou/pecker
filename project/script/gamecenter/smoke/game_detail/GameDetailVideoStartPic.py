# -*- coding: UTF-8 -*-

"""
File Name:      GameDetailVideoStartPic
Author:         zhangwei04
Create Date:    2018/11/30
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class GameDetailVideoStartPic(TestsuiteNormal):
    """
    预置条件：游戏中心首页配置的游戏有播放视频，游戏视频最好大于20秒，网络通畅
    """
    def setup(self):
        self.desc = "游戏详情-视频-头图"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info(self.data.game_name)
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.swipe_down_into_game_detail(self.data.game_name), "进入详情页有顶部视频的游戏", target=DUT)
        assert_true(DUT.GameDetailPage.check_video_start_img(self.data.game_name, self.data.pic_name), "检测视频头片", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

# -*- coding: UTF-8 -*-

"""
File Name:      PokerVideoPlay
Author:         zhangwei04
Create Date:    2018/12/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class PokerVideoPlay(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "棋牌-视频模板-视屏播放"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("视频模块标题：{}".format(self.data.video_title))
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.into_poker(), "进入棋牌中心", target=DUT)
        assert_true(DUT.PokerPage.check_ui(), "棋牌中心检测UI", target=DUT)
        assert_true(DUT.PokerPage.check_video_play(self.data.video_title), "视频模块检测视频播放", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

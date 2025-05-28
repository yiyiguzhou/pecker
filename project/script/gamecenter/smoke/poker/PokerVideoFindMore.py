# -*- coding: UTF-8 -*-

"""
File Name:      PokerVideoFindMore
Author:         zhangwei04
Create Date:    2018/12/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class PokerVideoFindMore(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "棋牌-视频模板-查看全部节目"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.into_poker(), "进入棋牌中心", target=DUT)
        assert_true(DUT.PokerPage.check_ui(), "棋牌中心检测UI", target=DUT)
        assert_true(DUT.PokerPage.click_video_template_find_more(self.data.video_title), "视频模块点击查看全部节目", target=DUT)
        assert_true(DUT.H5Page.check_topic_from_poker_video(self.data.topic_title), "查看跳转的H5专题页", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

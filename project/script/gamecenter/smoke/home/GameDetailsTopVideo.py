# -*- coding: UTF-8 -*-

"""
File Name:      GameDetailsTopVideo
Author:         gufangmei_sx
Create Date:    2018/8/22
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class GameDetailsTopVideo(TestsuiteNormal):
    """
    用例描述：游戏详情页-顶部视频
    预置条件：本周人气推荐的第一款游戏，配置了关联视频且用户处于wifi环境下
    """
    def setup(self):
        self.desc = "游戏详情页-顶部视频"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("本周人气推荐的第一款游戏，配置了关联视频且用户处于wifi环境下")
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.swipe_down_into_game_detail(self.data.game_name), "进入详情页有顶部视频的游戏", target=DUT)
        assert_true(DUT.HomePage.check_video(), "详情页视频播放", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
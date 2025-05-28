# -*- coding: UTF-8 -*-

"""
File Name:      HomeVideoGotoGD
Author:         gufangmei_sx
Create Date:    2018/8/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class HomeVideoGotoGD(TestsuiteNormal):
    """
    预置条件：首页配置了视频模块的游戏
    """
    def setup(self):
        self.desc = "首页-视频模板运-游戏详情页"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info(self.data.game_name)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.video_template_goto_game_detail(self.data.game_name), "从视频模块进入游戏详情页", target=DUT)
        assert_true(DUT.GameDetailPage.check_ui(self.data.game_name), "游戏详情页检测UI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
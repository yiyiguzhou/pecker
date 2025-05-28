# -*- coding: UTF-8 -*-

"""
File Name:      HorizontalGameRecommendation
Author:         gufangmei_sx
Create Date:    2018/7/9
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class HorizontalGameRecommendation(TestsuiteNormal):
    """
    用例描述：首页-横排游戏推荐位
    预置条件：奇玩1.0后台运营位：1350配置了横排游戏推荐位一的标题；运营位：1333配置了15款游戏。
    """
    def setup(self):
        self.desc = "首页-横排游戏推荐位"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.click_game_horizontal_first_icon(self.data.title), "点击横排[{}]第一个运营位".format(self.data.title), target=DUT)
        assert_true(DUT.Common.check_title(self.data.game_information), "检查游戏信息 ", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
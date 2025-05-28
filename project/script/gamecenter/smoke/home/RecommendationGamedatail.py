# -*- coding: UTF-8 -*-

"""
File Name:      LargePictureRecommendation
Author:         gufangmei_sx
Create Date:    2018/7/10
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class RecommendationGamedatail(TestsuiteNormal):
    """
    用例描述：首页-大图推荐模板运营位-进入游戏详情页
    预置条件：奇玩1.0后台大图推荐模板运营位一：1343配置进入游戏详情页。
    """
    def setup(self):
        self.desc = "首页-大图推荐模板运营位-进入游戏详情页"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info(self.data.game_introduction)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.large_picture_with_game_into(self.data.game_introduction), "点击大图进入详情页", target=DUT)
        assert_true(DUT.GameDetailPage.check_ui(self.data.game_name), "查看详情信息", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

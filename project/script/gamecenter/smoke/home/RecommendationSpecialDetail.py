# -*- coding: UTF-8 -*-

"""
File Name:      RecommendationSpecialDetail
Author:         gufangmei_sx
Create Date:    2018/7/10
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class RecommendationSpecialDetail(TestsuiteNormal):
    """
    用例描述：首页-大图推荐模板运营位-进入专题详情页
    预置条件：奇玩1.0后台大图推荐模板运营位二：1355配置进入专题详情页。
    """
    def setup(self):
        self.desc = "首页-大图推荐模板运营位-进入专题详情页"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.large_picture_without_game_into(self.data.game_introduction), "点击大图进入专题详情页", target=DUT)
        assert_true(DUT.Common.check_title(self.data.title), "查看专题标题", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
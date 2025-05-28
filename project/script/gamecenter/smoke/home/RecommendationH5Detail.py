# -*- coding: UTF-8 -*-

"""
File Name:      RecommendationH5Detail
Author:         gufangmei_sx
Create Date:    2018/7/25
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class RecommendationH5Detail(TestsuiteNormal):
    """
    用例描述：首页-大图推荐模板运营位-进入H5活动页
    预置条件：奇玩1.0后台大图推荐模板运营位三：1357配置进入H5活动页。
    """
    def setup(self):
        self.desc = "首页-大图推荐模板运营位-进入H5活动页"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("专题游戏描述：{}".format(self.data.game_introduction))
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.large_picture_without_game_into(self.data.game_introduction), "点击大图进入H5活动页", target=DUT)
        assert_true(DUT.Common.check_title(self.data.title), "查看H5页面标题", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
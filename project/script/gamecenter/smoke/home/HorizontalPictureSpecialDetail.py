# -*- coding: UTF-8 -*-

"""
File Name:      HorizontalPictureRecommendation
Author:         gufangmei_sx
Create Date:    2018/7/10
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class HorizontalPictureSpecialDetail(TestsuiteNormal):
    """
    用例描述：首页-横排图片模板运营位-进入专题详情页
    预置条件：奇玩1.0后台运营位：1369配置了横排图片推荐位一的标题；运营位：1345横排图片推荐位一配置了5个图片，其中的第一张图片配置了专题
    """
    def setup(self):
        self.desc = "首页-横排图片模板运营位-进入专题详情页"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("配置了横排图片推荐位一的标题")
        g_logger.info("横排名：{}".format(self.data.title))
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.Common.check_title(self.data.title, timeout=120), "横排图片专题推荐 ", target=DUT)
        assert_true(DUT.HomePage.click_picture_horizontal_first_icon(self.data.title), "检查专题推荐位一的标题", target=DUT)
        assert_true(DUT.Common.check_title(self.data.special_topic), "检查专题名称信息 ", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
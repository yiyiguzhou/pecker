# -*- coding: UTF-8 -*-

"""
File Name:      VipFocusImageEnterSpecialDetail
Author:         gufangmei_sx
Create Date:    2018/7/25
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class VipFocusImageEnterSpecialDetail(TestsuiteNormal):
    """
    用例描述：游戏会员页-焦点图进入专题详情页
    预置条件：奇玩1.0后台运营位：1300第四张轮播图配置进入专题详情页。
    """
    def setup(self):
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info("奇玩1.0后台运营位：1300第四张轮播图配置进入专题详情页。")
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.VipPage.into_vip_page(self.data.title), "进入游戏会员页", target=DUT)
        assert_true(DUT.VipPage.click_carousel_map3(self.data.special_title), "点击轮播图进入专题详情页", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
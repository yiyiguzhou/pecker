# -*- coding: UTF-8 -*-

"""
File Name:      BasePlayIPIntoGD
Author:         zhangwei04
Create Date:    2019/1/20
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class BasePlayIPIntoGD(TestsuiteNormal):
    """
    预置条件：视频带有关联游戏，VIP账户登录
    """
    def setup(self):
        self.desc = "基线-搜索-IP关联位-游戏详情页"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Login.base_login_out(), "退出登录", target=DUT)
        assert_true(DUT.Login.base_login_in(account_section='vip'), "VIP账户登录", target=DUT)
        assert_true(DUT.BasePage.click_bottom_home(), "点击底部首页", target=DUT)
        assert_true(DUT.BasePage.click_home_search_button(), "点击搜索框进入搜索页", target=DUT)
        assert_true(DUT.BasePage.search_page_search_text(self.data.video_name), "搜索页搜索视频", target=DUT)
        assert_true(DUT.BasePage.search_page_click_associate_text(self.data.video_name), "根据联想词进入视频详情页", target=DUT)
        assert_true(DUT.BasePage.video_detail_click_play(), "视频详情页点击播放进入视频播放页", target=DUT)
        assert_true(DUT.BasePage.video_play_into_game(self.data.game_name), "视频播放页点击IP关联位进入游戏详情页", target=DUT)
        assert_true(DUT.GameDetailPage.check_ui(self.data.game_name), "检测游戏详情页UI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

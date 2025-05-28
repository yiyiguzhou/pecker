# -*- coding: UTF-8 -*-

"""
File Name:      BaseSearchRelatedIntoGD
Author:         zhangwei04
Create Date:    2019/1/20
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class BaseSearchRelatedIntoGD(TestsuiteNormal):
    """
    预置条件：游戏有福利和游戏圈, 桌面设置成循环滑动
    """
    def setup(self):
        self.desc = "基线-搜索-游戏关联位-游戏详情页"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.BasePage.click_home_search_button(), "点击搜索框进入搜索页", target=DUT)
        assert_true(DUT.BasePage.search_page_search_text(self.data.video_name), "搜索页查询视频", target=DUT)
        assert_true(DUT.BasePage.search_page_click_associate_text(self.data.video_name), "根据联想词进入视频详情页", target=DUT)
        assert_true(DUT.BasePage.video_detail_in_game_detail(self.data.game_name), "视频详情页进入游戏详情页", target=DUT)
        assert_true(DUT.GameDetailPage.check_ui(self.data.game_name), "检测游戏中心首页UI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

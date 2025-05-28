# -*- coding: UTF-8 -*-

"""
File Name:      GameDetailIntoH5Game
Author:         zhangwei04
Create Date:    2018/11/30
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class GameDetailIntoH5Game(TestsuiteNormal):
    """
    预置条件：选择有关联的H5游戏
    """
    def setup(self):
        self.desc = "游戏详情-免下载畅玩"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.swipe_down_into_game_detail(self.data.game_name), "进入详情页有顶部视频的游戏", target=DUT)
        assert_true(DUT.GameDetailPage.click_play_without_download(), "点击免下载畅玩按钮", target=DUT)
        assert_true(DUT.H5Page.check_game_ui(), "检测H5游戏UI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

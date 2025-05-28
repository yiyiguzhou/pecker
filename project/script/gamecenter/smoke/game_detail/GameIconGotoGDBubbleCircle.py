# -*- coding: UTF-8 -*-

"""
File Name:      GameIconGotoGDBubbleCircle
Author:         zhangwei04
Create Date:    2018/11/30
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class GameIconGotoGDBubbleCircle(TestsuiteNormal):
    """
    预置条件：游戏详情页有福利和游戏圈
    """
    def setup(self):
        self.desc = "游戏详情-游戏圈-已安装进入游戏圈"
        DUT.device.start_log()
        DUT.Common.uninstall_game_from_conf(self.data.game_name)
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.swipe_down_into_game_detail(self.data.game_name, check_text="游戏圈"), "进入游戏详情页", target=DUT)
        assert_true(DUT.GameDetailPage.game_download_and_install(self.data.game_name, open_game=False), "下载、安装游戏", target=DUT)
        time.sleep(2)
        DUT.Common.reset_app()
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.swipe_down_into_game_detail(self.data.game_name), "进入详情页有福利和游戏圈的游戏", target=DUT)
        time.sleep(5)  # 等待页面加载稳定
        assert_true(DUT.GameDetailPage.check_bubble_circle_tab(), "检测是否是进入游戏圈Tab", target=DUT)

        assert_true(DUT.GameDetailPage.uninstall_app(app_name=self.data.game_name), "卸载游戏", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

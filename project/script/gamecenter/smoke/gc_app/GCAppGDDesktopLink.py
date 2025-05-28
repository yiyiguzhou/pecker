# -*- coding: UTF-8 -*-

"""
File Name:      GCAppGDDesktopLink
Author:         zhangwei04
Create Date:    2018/11/30
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class GCAppGDDesktopLink(TestsuiteNormal):
    """
    预置条件：游戏有福利和游戏圈
    """
    def setup(self):
        self.desc = "分发App-游戏详情-创建桌面快捷方式"
        DUT.device.start_log()
        DUT.Common.uninstall_gc_app()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.swipe_down_into_game_detail(self.data.game_name), "进入详情页", target=DUT)
        assert_true(DUT.GameDetailPage.get_gc_app(), "查看并安装分发app", target=DUT)
        assert_true(DUT.Common.check_desktop_gc(), "返回桌面，查看快捷方式", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

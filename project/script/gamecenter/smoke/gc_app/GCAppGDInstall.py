# -*- coding: UTF-8 -*-

"""
File Name:      GCAppGDInstall
Author:         zhangwei04
Create Date:    2018/11/30
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class GCAppGDInstall(TestsuiteNormal):
    """
    预置条件：游戏有福利和游戏圈
    """
    def setup(self):
        self.desc = "分发App-游戏详情-显示&安装"
        DUT.device.start_log()
        DUT.Common.uninstall_gc_app()
        DUT.Common.uninstall_game_from_conf(self.data.game_name)
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.swipe_down_into_game_detail(self.data.game_name), "进入详情页", target=DUT)
        time.sleep(5)
        assert_true(DUT.GameDetailPage.get_gc_app(), "查看并安装分发app", target=DUT)
        g_logger.info("重置基线app，进入游戏详情页，查看分发app是否显示")
        DUT.Common.cmd_back()
        DUT.Common.reset_app()
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.swipe_down_into_game_detail(self.data.game_name), "进入详情页", target=DUT)
        assert_false(DUT.GameDetailPage.check_gc_app_display(), "查看没有显示分发app按钮", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

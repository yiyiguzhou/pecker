# -*- coding: UTF-8 -*-

"""
File Name:      GCAppDesktopInto
Author:         zhangwei04
Create Date:    2018/11/30
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class GCAppDesktopInto(TestsuiteNormal):
    """
    预置条件：游戏有福利和游戏圈, 桌面设置成循环滑动
    """
    def setup(self):
        self.desc = "分发App-桌面进入原界面"
        DUT.device.start_log()
        DUT.Common.uninstall_game_from_conf(self.data.game_name)
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info(self.data.game_name)
        # if not DUT.Common.check_gc_app_is_installed():
        #     g_logger.info("检测到分发app未安装，adb方式安装分发app")
        assert_true(DUT.Common.install_app("com.qiyi.gcapp.apk", uninstall_flag=True), "安装最新的分发app", target=DUT)
        time.sleep(3)

        assert_true(DUT.Common.desktop_into_gc(), "从桌面进入分发app", target=DUT)
        time.sleep(3)
        assert_true(DUT.HomePage.swipe_down_into_game_detail(self.data.game_name), "进入详情页", target=DUT)
        assert_true(DUT.GameDetailPage.check_ui(self.data.game_name), "检测游戏详情页UI", target=DUT)
        assert_true(DUT.Common.desktop_into_gc(), "退回桌面，从桌面进入分发app", target=DUT)
        for i in range(2):  # 向下滑动，保证游戏信息能够找到
            DUT.Common.device.swipe_screen(rate=0.4, direction='down')
        assert_true(DUT.GameDetailPage.check_ui(self.data.game_name), "检测游戏详情页UI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

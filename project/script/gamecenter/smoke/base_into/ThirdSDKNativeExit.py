# -*- coding: UTF-8 -*-

"""
File Name:      ThirdSDKNativeExit
Author:         zhangwei04
Create Date:    2019/1/20
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class ThirdSDKNativeExit(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "第三方SDK-Native-退出游戏"
        DUT.device.start_log()
        DUT.Common.uninstall_game_from_conf(self.data.game_name)
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("游戏：{}".format(self.data.game_name))
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.swipe_down_into_game_detail(self.data.game_name), "进入游戏详情页", target=DUT)
        assert_true(DUT.GameDetailPage.game_download_and_install(self.data.game_name, open_game=True, close_game=False), "游戏下载安装并打开", target=DUT)
        time.sleep(10)
        assert_true(DUT.GamePage.into_exiting_native_game(), "进入Native游戏退出界面", target=DUT)
        assert_true(DUT.GamePage.click_native_exit(), "游戏退出点击退出", target=DUT)
        assert_true(DUT.GameDetailPage.check_ui(self.data.game_name), "检测前一个页面游戏详情页UI", target=DUT)

    def teardown(self):
        DUT.GameDetailPage.uninstall_game(self.data.game_name)
        DUT.device.stop_log()

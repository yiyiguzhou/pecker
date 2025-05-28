# -*- coding: UTF-8 -*-

"""
File Name:      ThirdSDKNativeMoreGameGotoGC
Author:         zhangwei04
Create Date:    2019/1/20
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class ThirdSDKNativeMoreGameGotoGC(TestsuiteNormal):
    """
    预置条件：游戏退出大图跳转配置的是游戏中心
    """
    def setup(self):
        self.desc = "第三方SDK-Native-更多游戏-游戏中心"
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
        assert_true(DUT.GamePage.click_native_exit_more_game(), "游戏退出点击更多游戏", target=DUT)
        assert_true(DUT.HomePage.check_ui(), "检测是否进入游戏中心首页", target=DUT)

    def teardown(self):
        DUT.GameDetailPage.uninstall_game(self.data.game_name)
        DUT.device.stop_log()

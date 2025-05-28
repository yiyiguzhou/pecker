# -*- coding: UTF-8 -*-

"""
File Name:      HomeFullScreenInstalledGame
Author:         zhangwei04
Create Date:    2018/11/29
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class HomeFullScreenInstalledGame(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "首页-全屏弹窗-已安装游戏"
        DUT.device.start_log()
        DUT.Common.clear_app_data(launch_app=True)

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.HomePage.into_game_center_without_check(), "进入游戏中心,不检测UI", target=DUT)
        assert_true(DUT.HomePage.full_screen_download(game_type=self.data.game_type, game_name=self.data.game_name, uninstall=False), desc="全屏弹窗下载安装游戏", target=DUT)
        assert_true(DUT.HomePage.clear_app_data(launch_app=True), desc="清除App数据")
        assert_true(DUT.HomePage.into_game_center_without_check(), "进入游戏中心,不检测UI", target=DUT)
        assert_true(DUT.HomePage.check_full_screen_not_pull(self.data.newgame), "通过检测到新游确认没有游戏弹窗", target=DUT)
        assert_true(DUT.HomePage.uninstall_game(self.data.game_name), "卸载游戏")
        assert_true(DUT.HomePage.reset_app(), "重启app关闭全屏弹窗")
        DUT.HomePage.into_game_center_without_check()
        DUT.HomePage.full_screen_close()

    def teardown(self):
        DUT.HomePage.uninstall_game(self.data.game_name)
        DUT.device.stop_log()

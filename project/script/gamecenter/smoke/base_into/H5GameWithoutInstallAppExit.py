# -*- coding: UTF-8 -*-

"""
File Name:      H5GameWithoutInstallAppExit
Author:         zhangwei04
Create Date:    2019/1/20
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class H5GameWithoutInstallAppExit(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "H5游戏-未下载APP-退出-正常退出"
        DUT.device.start_log()
        DUT.Common.uninstall_app_from_conf(self.data.app_name)
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.into_small_game_module(), "进入小游戏中心", target=DUT)
        assert_true(DUT.Common.into_download_manager(), "进入下载管理器", target=DUT)
        g_logger.info("检测是否有已经下载了小游戏App, 若下载则移除掉")
        DUT.DownloadManager.rm_will_install_app(self.data.app_name)
        assert_true(DUT.Common.back_to_homepage(), "退出下载管理器至游戏中心", target=DUT)
        assert_true(DUT.HomePage.into_small_game_module(), "再次进入小游戏中心", target=DUT)

        assert_true(DUT.SmallGamePage.click_game(self.data.game_name), "点击小游戏", target=DUT)
        time.sleep(10)  # 等待10秒小游戏加载，小游戏app下载安装
        assert_true(DUT.GamePage.game_install(self.data.app_name, confirm_guide=False), "进入小游戏时，弹出安装页面安装游戏", target=DUT)
        assert_true(DUT.GamePage.back_to_h5_exit_page(), "点掉安装完成页面，回退到退出游戏页面", target=DUT)
        assert_true(DUT.GamePage.click_h5_exit(), "点击退出游戏", target=DUT)
        assert_true(DUT.SmallGamePage.check_ui(), "检测小游戏中心UI，确认退出了游戏", target=DUT)

    def teardown(self):
        DUT.GameDetailPage.uninstall_game(self.data.game_name)
        DUT.device.stop_log()

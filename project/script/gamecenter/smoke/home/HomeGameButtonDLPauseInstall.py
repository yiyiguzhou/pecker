# -*- coding: UTF-8 -*-

"""
File Name:      HomeGameButtonDLPauseInstall
Author:         zhangwei04
Create Date:    2018/11/29
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class HomeGameButtonDLPauseInstall(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "首页-按钮状态-下载暂停继续安装"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info(self.data.game_name)
        assert_true(DUT.HomePage.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        DUT.HomePage.into_download_manager()
        DUT.DownloadManager.rm_will_install_app(self.data.game_name)
        DUT.Common.cmd_back()
        time.sleep(3)
        assert_true(DUT.HomePage.swipe_down_into_game_detail(game_name=self.data.game_name), desc="进入游戏详情页", target=DUT)
        assert_true(DUT.GameDetailPage.check_ui(game_name=self.data.game_name, sys_require=None), desc="检测游戏详情页UI", target=DUT)
        assert_true(DUT.GameDetailPage.game_downlaod_pause_install(self.data.game_name, open_game=True), desc="游戏下载、暂停、安装、打开", target=DUT)

    def teardown(self):
        assert_true(DUT.GameDetailPage.uninstall_game(self.data.game_name), "卸载游戏", target=DUT)
        DUT.Common.cmd_back()
        DUT.device.stop_log()

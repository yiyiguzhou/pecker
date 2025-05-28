# -*- coding: UTF-8 -*-

"""
File Name:      HomeGameButtonUpdate
Author:         zhangwei04
Create Date:    2018/11/29
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class HomeGameButtonUpdate(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "首页-下载管理器-更新游戏"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info(self.data.game_name)
        assert_true(DUT.HomePage.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.into_download_manager(), desc="进入游戏详情页", target=DUT)
        assert_true(DUT.DownloadManager.check_ui(), desc="检测下载管理器UI，确保进入下载管理器", target=DUT)
        assert_true(DUT.DownloadManager.update_game(game_name=self.data.game_name), desc="游戏更新")

    def teardown(self):
        DUT.device.stop_log()

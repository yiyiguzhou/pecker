# -*- coding: UTF-8 -*-

"""
File Name:      HomeIntoConfPortURL
Author:         zhangwei04
Create Date:    2018/11/19
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class HomeDLManagerDLTab(TestsuiteNormal):
    """
    用例描述：首页-下载管理-下载Tab
    预置条件：无
    """
    def setup(self):
        self.desc = "首页-下载管理-下载Tab"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.HomePage.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.into_download_manager(), "进入游戏下载管理器", target=DUT)
        assert_true(DUT.DownloadManager.check_download_tab(), desc="检测下载tab", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
# -*- coding: UTF-8 -*-

"""
File Name:      DownloadManager
Author:         gufangmei_sx
Create Date:    2018/7/6
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class DownloadManager(TestsuiteNormal):
    """
     预置条件：
    """

    def setup(self):
        self.desc = "首页-顶部栏下载管理器按钮"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        time.sleep(5)
        assert_true(DUT.HomePage.into_download_manager(), "进入下载管理器", target=DUT)
        assert_true(DUT.DownloadManager.check_ui(), "检测UI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
# -*- coding: UTF-8 -*-

"""
File Name:      HomeFullScreeIntoGame
Author:         zhangwei04
Create Date:    2018/11/19
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class HomeFullScreeIntoGame(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "首页-全屏弹窗-游戏下载安装进入"
        DUT.device.start_log()
        DUT.Common.clear_app_data(launch_app=True)
        # time.sleep(3)
        # DUT.Common.reset_app()
        # DUT.Common.device.swipe_screen()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.HomePage.into_game_center_without_check(), "进入游戏中心,不检测UI", target=DUT)
        assert_true(DUT.HomePage.full_screen_download(game_type=self.data.game_type, game_name=self.data.game_name), desc="全屏弹窗进入游戏", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

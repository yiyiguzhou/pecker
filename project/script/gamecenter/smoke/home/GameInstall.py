# -*- coding: UTF-8 -*-

"""
File Name:      GameInstall
Author:         gufangmei_sx
Create Date:    2018/9/30
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class GameInstall(TestsuiteNormal):
    """
    用例描述：游戏安装
    预置条件：
    """
    def setup(self):
        self.desc = "游戏安装"
        DUT.device.start_log()
        DUT.Common.reset_app("com.qiyi.video", "com.qiyi.video.WelcomeActivity")

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.HomePage.game_install(), "安装游戏", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
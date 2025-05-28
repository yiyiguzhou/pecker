# -*- coding: UTF-8 -*-

"""
File Name:      HomeFullScreenOnce
Author:         zhangwei04
Create Date:    2018/11/19
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class HomeFullScreenOnce(TestsuiteNormal):
    """
    用例描述：首页-只全屏弹窗一次
    预置条件：无
    """
    def setup(self):
        self.desc = "首页-只全屏弹窗一次"
        DUT.device.start_log()
        DUT.Common.clear_app_data(launch_app=True)

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.HomePage.into_game_center_without_check(), "进入游戏中心,不检测UI", target=DUT)
        assert_true(DUT.HomePage.full_screen_close(), desc="关闭全屏弹窗", target=DUT)
        DUT.device.adb.adb_shell('input keyevent KEYCODE_HOME')
        g_logger.info("等待10秒，否则可能会弹出基线授权弹窗")
        time.sleep(10)
        DUT.Common.reset_app(pkg='com.qiyi.video', activity="com.qiyi.video.WelcomeActivity")
        assert_true(DUT.HomePage.into_game_center(self.data.newgame), "进入游戏中心,检测新游", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
# -*- coding: UTF-8 -*-

"""
File Name:      InstallAPK
Author:         zhangwei04
Create Date:    2018/9/17
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class InstallAPK(TestsuiteNormal):
    def setup(self):
        self.desc = "安装基线apk-push游戏中心apk"
        DUT.device.start_log()

    def test(self):
        DUT.Common.install_base_apk()
        DUT.Common.ansy_catch_ad()

        g_logger.info("等待20秒，捕获广告")
        time.sleep(20)

        for i in range(2):
            DUT.Common.reset_app("com.qiyi.video", "com.qiyi.video.WelcomeActivity")
            g_logger.info("sleep 10 seconds for waiting loading gamecenter plugin")
            time.sleep(10)
            DUT.Common.into_game_center(self.data.newgame, self.data.poker)
            time.sleep(15)

        DUT.Common.stop_catch_ad()

    def teardown(self):
        DUT.Common.stop_catch_ad()
        DUT.device.stop_log()
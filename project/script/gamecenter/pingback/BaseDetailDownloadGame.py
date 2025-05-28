# -*- coding: UTF-8 -*-

"""
File Name:      DownloadGamePressure
Author:         zhangwei04
Create Date:    2018/9/29
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class BaseDetailDownloadGame(TestsuiteNormal):
    def setup(self):
        DUT.Pingback.reset_app()
        DUT.device.start_log()
        self.load_data(os.path.join(os.path.dirname(__file__), "BaseDownloadGame.xml"))  # 加载用例数据文件

    def test(self):
        assert_true(DUT.Pingback.into_game_center(), target=DUT)
        assert_true(DUT.Pingback.gamecenter_into_new_game(), target=DUT)

    def teardown(self):
        DUT.device.stop_log()
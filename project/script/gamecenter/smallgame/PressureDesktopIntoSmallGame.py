# -*- coding: UTF-8 -*-

"""
File Name:      PressureIntoSmallGame
Author:         zhangwei04
Create Date:    2018/8/29
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class PressureDesktopIntoSmallGame(TestsuiteNormal):
    def setup(self):
        pass

    def test(self):
        assert_true(DUT.SmallGame.into_desktop_small_game_app(), desc="从桌面快捷方式进入小游戏中心", target=DUT)
        for i in range(int(self.data.loop_times)):
            g_logger.info("loop_times: {}".format(i+1))
            expect_true(DUT.SmallGame.into_h5_game_from_samll_game_app(self.data.game_name), desc="进入小游戏{}".format(self.data.game_name), target=DUT)
            expect_true(DUT.SmallGame.out_game_from_sider(), desc="侧边栏退出", target=DUT)

    def teardown(self):
        pass

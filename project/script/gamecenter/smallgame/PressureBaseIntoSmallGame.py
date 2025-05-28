# -*- coding: UTF-8 -*-

"""
File Name:      PressureIntoSmallGame
Author:         zhangwei04
Create Date:    2018/8/29
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class PressureBaseIntoSmallGame(TestsuiteNormal):
    def setup(self):
        DUT.SmallGame.init()

    def test(self):
        # 从基线进入小游戏中心
        self.load_data(os.path.join(os.path.dirname(__file__), "PressureDesktopIntoSmallGame.xml"))     # 加载用例数据文件
        for i in range(int(self.data.loop_times)):
            g_logger.info("loop_times: {}".format(i+1))
            expect_true(DUT.SmallGame.into_h5_game_from_samll_game_app(self.data.game_name), desc="进入小游戏{}".format(self.data.game_name), target=DUT)
            expect_true(DUT.SmallGame.out_game_from_sider(), desc="侧边栏退出", target=DUT)

    def teardown(self):
        pass

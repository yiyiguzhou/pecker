# -*- coding: UTF-8 -*-

"""
File Name:      EnterGameCenter
Author:         gufangmei_sx
Create Date:    2018/7/6
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class EnterGameCenter(TestsuiteNormal):
    """
    用例描述：进入游戏中心首页
    预置条件：
    """
    def setup(self):
        self.desc = "进入游戏中心首页"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        time.sleep(1)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
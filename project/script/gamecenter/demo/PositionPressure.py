# -*- coding: UTF-8 -*-

"""
File Name:      AuthPresure
Author:         zhangwei04
Create Date:    2018/3/1
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class PositionPressure(TestsuiteNormal):
    """压测运营位脚本"""
    def setup(self):
        DUT.device.start_log()
        pass

    def test(self):
        g_logger.info('压测下载先重启APP确保是从基线版本进入, 进入基线脚本页面')
        assert_true(DUT.Demo.reset_app(), "重置app")
        g_logger.info("进入游戏中心界面")
        assert_true(DUT.Demo.into_game_center(), "进入游戏中心")

        g_logger.info('运营位压测')
        assert_true(DUT.Demo.in_game_center_first_pos_out(loop_times=1), '运营位压测')
        # import random
        # if random.randint(0, 3) % 3 == 0:
        #     # expect_true(False, desc="testfalse", target=DUT)
        #     raise Exception("testcase exception")

    def teardown(self):
        DUT.device.stop_log()
        pass
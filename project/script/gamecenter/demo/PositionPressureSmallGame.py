# -*- coding: UTF-8 -*-

"""
File Name:      AuthPresure
Author:         zhangwei04
Create Date:    2018/3/1
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class PositionPressureSmallGame(TestsuiteNormal):
    def setup(self):
        DUT.device.start_log()

    def test(self):
        g_logger.info('压测下载先重启APP确保是从基线版本进入, 进入基线脚本页面')
        assert_true(DUT.Demo.reset_app(), "重置app")
        g_logger.info("进入游戏中心界面")
        assert_true(DUT.Demo.into_game_center(), "进入游戏中心")
        g_logger.info('进入分类')
        assert_true(DUT.Demo.into_classify_game_center(), '进入分类')
        g_logger.info('进入小游戏')

        DUT.Demo.clear_buff_data()

    def teardown(self):
        DUT.device.stop_log()

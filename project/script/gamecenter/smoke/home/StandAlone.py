# -*- coding: UTF-8 -*-

"""
File Name:      StandAlone
Author:         gufangmei_sx
Create Date:    2018/8/9
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class StandAlone(TestsuiteNormal):
    """
    用例描述：首页-子业务入口-单机入口
    预置条件：
    """
    def setup(self):
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        self.desc = "首页-子业务入口-单机入口"
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        for button_name, title in zip(self.data.button_name, self.data.title):
            ret = DUT.Common.click_and_check(button_name, title)
            if ret:
                g_logger.info("进入单机页成功")
                break
        else:
            assert_true(False, "进入单机页失败", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
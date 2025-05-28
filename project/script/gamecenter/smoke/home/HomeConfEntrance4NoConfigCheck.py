# -*- coding: UTF-8 -*-

"""
File Name:      HomeIntoConfPortURL
Author:         zhangwei04
Create Date:    2018/11/19
"""
from project.script.testsuite.TestsuiteNormal import *


class HomeConfEntrance4NoConfigCheck(TestsuiteNormal):
    """
    预置条件：可配置入口4上配置了对应的图片和描述
    """
    def setup(self):
        self.desc = "首页-可配置子业务入口4未配置检测"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("可配置入口：4")
        assert_true(DUT.HomePage.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        time.sleep(3)
        assert_true(DUT.HomePage.into_configurable_entrance(self.data.entrance_number), "进入可配置入口4", target=DUT)
        assert_true(DUT.HomePage.check_woman_ui(), "检测女生版游戏中心UI", target=DUT)


    def teardown(self):
        DUT.device.stop_log()
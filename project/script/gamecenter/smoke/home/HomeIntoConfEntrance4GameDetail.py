# -*- coding: UTF-8 -*-

"""
File Name:      HomeIntoConfPortURL
Author:         zhangwei04
Create Date:    2018/11/19
"""
from project.script.testsuite.TestsuiteNormal import *


class HomeIntoConfEntrance4GameDetail(TestsuiteNormal):
    """
    预置条件：可配置入口上配置了对应的游戏详情页链接
    """
    def setup(self):
        self.desc = "首页-可配置子业务入口4-游戏详情页"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("可配置入口：{}".format(self.data.entrance_number))
        assert_true(DUT.HomePage.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.into_configurable_entrance(self.data.entrance_number), "进入可配置入口游戏详情页", target=DUT)
        assert_true(DUT.GameDetailPage.check_ui(self.data.game_name), desc="检测游戏详情页UI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
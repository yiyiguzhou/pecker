# -*- coding: UTF-8 -*-

"""
File Name:      HomeIntoConfPortURL
Author:         zhangwei04
Create Date:    2018/11/19
"""
from project.script.testsuite.TestsuiteNormal import *


class HomeIntoConfEntrance5URL(TestsuiteNormal):
    """
    用例描述：首页-可配置子业务入口-活动页
    预置条件：可配置入口上配置了对应的活动页链接
    """
    def setup(self):
        self.desc = "首页-可配置子业务入口5-活动页"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("可配置入口：{}".format(self.data.entrance_number))
        assert_true(DUT.HomePage.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.into_configurable_entrance(self.data.entrance_number), "进入可配置入口H5活动页", target=DUT)
        assert_true(DUT.H5Page.check_ui(), "检测H5页面UI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
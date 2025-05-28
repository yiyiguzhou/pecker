# -*- coding: UTF-8 -*-

"""
File Name:      H5PageEnterNativeGame
Author:         gufangmei_sx
Create Date:    2018/8/16
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class H5PageEnterNativeGame(TestsuiteNormal):
    """
    用例描述：首页-可配置子业务入口-H5页面功能-进入Native游戏详情页
    预置条件：首页子业务入口配置一个可进入Native游戏详情页的H5页面。
    """
    def setup(self):
        self.desc = "首页-可配置子业务入口-H5页面功能-进入Native游戏详情页"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.into_configurable_entrance(self.data.entrace_number, self.data.title), "进入可配置入口H5活动页", target=DUT)
        # assert_true(DUT.HomePage.click_H5_picture(self.data.game_name, self.data.details), "点击H5页面上的游戏图片进入游戏详情页", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
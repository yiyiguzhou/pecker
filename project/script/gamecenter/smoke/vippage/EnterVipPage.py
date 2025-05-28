# -*- coding: UTF-8 -*-

"""
File Name:      EnterVipPage
Author:         gufangmei_sx
Create Date:    2018/7/12
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class EnterVipPage(TestsuiteNormal):
    """
    预置条件：
    """
    def setup(self):
        self.desc = "首页子业务入口进入游戏会员页"
        DUT.device.start_log()
        DUT.Co.reset_app()

    def test(self):
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.VipPage.into_vip_page(self.data.entrance, self.data.title), "进入游戏会员页", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
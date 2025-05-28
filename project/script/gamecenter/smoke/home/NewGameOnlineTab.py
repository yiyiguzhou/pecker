# -*- coding: UTF-8 -*-

"""
File Name:      NewGameOnlineTab
Author:         gufangmei_sx
Create Date:    2018/8/10
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class NewGameOnlineTab(TestsuiteNormal):
    """
    用例描述：新游页-最新上线tab
    预置条件：运营位：1486配置了6款游戏。
    """
    def setup(self):
        self.desc = "新游页-最新上线tab"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.into_new_game(), "进入新游", target=DUT)
        assert_true(DUT.Common.check_title_xpath(self.data.title), "检查新游推荐标题", target=DUT)
        assert_true(DUT.HomePage.check_newgame_online_tab(), "按顺序检查本月新游，季度新游", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
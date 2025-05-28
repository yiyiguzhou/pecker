# -*- coding: UTF-8 -*-

"""
File Name:      NewGameUI
Author:         gufangmei_sx
Create Date:    2018/8/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class NewGameUI(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "新游UI"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        # assert_true(DUT.HomePage.enter_setting(), "进入个人中心设置页面", target=DUT)
        # assert_true(DUT.MyInfoPage.switch_environment("online"), "切换至线上环境", target=DUT)
        # assert_true(DUT.MyInfoPage.setting_back_to_home(), "返回至主页", target=DUT)
        assert_true(DUT.HomePage.into_new_game(), "进入新游页", target=DUT)
        assert_true(DUT.NewGamePage.check_ui(), "检查新游标题", target=DUT)
        assert_true(DUT.NewGamePage.check_up_to_date_tab_ui(), "检测最新上线Tab UI", target=DUT)
        # assert_true(DUT.HomePage.enter_setting(), "进入个人中心设置页面", target=DUT)
        # assert_true(DUT.MyInfoPage.switch_back_environment(), "切回环境", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
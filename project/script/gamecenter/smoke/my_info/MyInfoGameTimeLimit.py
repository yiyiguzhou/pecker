# -*- coding: UTF-8 -*-

"""
File Name:      MyInfoGameTimeLimit
Author:         zhangwei04
Create Date:    2018/1/2
"""
import time
# from project.script.testsuite.TestsuiteNormal import *
from project.script.gamecenter.testsuite.TestsuiteMyInfo import *


class MyInfoGameTimeLimit(TestsuiteMyInfo):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "个人中心-设置-游戏控制"
        DUT.device.start_log()
        # DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        # assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.Common.back_to_homepage())
        assert_true(DUT.HomePage.into_my_info(), "进入个人中心", target=DUT)

        assert_true(DUT.MyInfoPage.click_setting(), "个人中心页点击设置图标", target=DUT)
        assert_true(DUT.MyInfoPage.check_setting_ui(), "设置页检测UI", target=DUT)
        assert_true(DUT.MyInfoPage.setting_into_game_time_limit(), "进入游玩时间控制页", target=DUT)
        assert_true(DUT.MyInfoPage.open_game_time_limit(), "游玩时间控制页打开控制开关", target=DUT)
        assert_true(DUT.MyInfoPage.back_common_title(), "游玩时间控制页回退至设置页", target=DUT)
        assert_true(DUT.MyInfoPage.setting_check_game_time_limit_open(), "设置页检测游戏控制开关", target=DUT)
        assert_true(DUT.MyInfoPage.setting_into_game_time_limit(), "进入游玩时间控制页", target=DUT)
        assert_true(DUT.MyInfoPage.close_game_time_limit(), "游玩时间控制页关闭控制开关", target=DUT)
        assert_true(DUT.MyInfoPage.back_common_title(), "游玩时间控制页回退至设置页", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

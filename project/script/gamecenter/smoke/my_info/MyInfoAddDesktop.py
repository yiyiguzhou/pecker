# -*- coding: UTF-8 -*-

"""
File Name:      MyInfoAddDesktop
Author:         zhangwei04
Create Date:    2018/1/2
"""
import time
from project.script.gamecenter.testsuite.TestsuiteMyInfo import *


class MyInfoAddDesktop(TestsuiteMyInfo):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "个人中心-设置-添加GC到桌面"
        DUT.device.start_log()
        # DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        # assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.Common.back_to_homepage())
        assert_true(DUT.HomePage.into_my_info(), "进入个人中心", target=DUT)

        assert_true(DUT.MyInfoPage.click_setting(), "个人中心页点击设置图标", target=DUT)
        assert_true(DUT.MyInfoPage.check_setting_ui(), "设置页检测UI", target=DUT)
        assert_true(DUT.MyInfoPage.check_setting_shortcut(), "检测添加快捷方式功能", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

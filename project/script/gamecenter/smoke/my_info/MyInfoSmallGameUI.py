# -*- coding: UTF-8 -*-

"""
File Name:      MyInfoSmallGameUI
Author:         zhangwei04
Create Date:    2018/1/2
"""
import time
# from project.script.testsuite.TestsuiteNormal import *
from project.script.gamecenter.testsuite.TestsuiteMyInfo import *


class MyInfoSmallGameUI(TestsuiteMyInfo):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "个人中心-小游戏UI"
        DUT.device.start_log()
        # DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        # assert_true(DUT.Login.base_login_out(), "退出登录", target=DUT)
        # assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        # assert_true(DUT.Login.into_login_page(), "进入游戏中心登录页面", target=DUT)
        # assert_true(DUT.Login.login_in_with_password(account_section="phone_1"), "密码登录", target=DUT)
        assert_true(DUT.Common.back_to_homepage())
        assert_true(DUT.HomePage.into_my_info(), "进入个人中心", target=DUT)
        assert_true(DUT.MyInfoPage.click_tab(self.data.tab_name), "点击小游戏标签", target=DUT)
        assert_true(DUT.MyInfoPage.check_tab_ui(tab_name=self.data.tab_name, game_name=self.data.game_name), "检测小游戏tabUI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

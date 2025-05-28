# -*- coding: UTF-8 -*-

"""
File Name:      MyInfoPlayedDL
Author:         zhangwei04
Create Date:    2018/1/2
"""
import time
# from project.script.testsuite.TestsuiteNormal import *
from project.script.gamecenter.testsuite.TestsuiteMyInfo import *


class MyInfoPlayedDL(TestsuiteMyInfo):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "个人中心-已完过-游戏下载&打开"
        DUT.device.start_log()
        DUT.Common.uninstall_game_from_conf(self.data.game_name)
        # DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info(self.data.game_name)
        time.sleep(5)
        # assert_true(DUT.Login.base_login_out(), "退出登录", target=DUT)
        # assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        # assert_true(DUT.Login.into_login_page(), "进入游戏中心登录页面", target=DUT)
        # assert_true(DUT.Login.login_in_with_password(account_section="phone_1"), "密码登录", target=DUT)
        assert_true(DUT.Common.back_to_homepage())
        assert_true(DUT.HomePage.into_my_info(), "进入个人中心", target=DUT)

        # assert_true(DUT.MyInfoPage.check_default_tab_ui(game_name=self.data.game_name), "个人中心检测UI", target=DUT)
        assert_true(DUT.MyInfoPage.vertical_game_button_install(self.data.game_name, direction='down'), "点击游戏下载按钮进行下载或更新", target=DUT)
        time.sleep(2)
        assert_true(DUT.MyInfoPage.vertical_game_open(self.data.game_name), "点击游戏打开按钮，打开游戏", target=DUT)
        time.sleep(5)
        assert_false(DUT.MyInfoPage.check_default_tab_ui(game_name=self.data.game_name, timeout=10), "检测不在个人中心UI", target=DUT)

    def teardown(self):
        DUT.MyInfoPage.uninstall_game(self.data.game_name)
        time.sleep(2)
        DUT.device.stop_log()

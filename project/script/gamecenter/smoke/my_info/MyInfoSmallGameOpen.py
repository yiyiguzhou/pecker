# -*- coding: UTF-8 -*-

"""
File Name:      MyInfoSmallGameOpen
Author:         zhangwei04
Create Date:    2018/1/2
"""
import time
# from project.script.testsuite.TestsuiteNormal import *
from project.script.gamecenter.testsuite.TestsuiteMyInfo import *


class MyInfoSmallGameOpen(TestsuiteMyInfo):
    """
    预置条件：小游戏app中心已经安装
    """
    def setup(self):
        self.desc = "个人中心-小游戏-打开H5游戏"
        DUT.device.start_log()
        # DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("预置条件：小游戏app中心已经安装")
        g_logger.info("游戏名：{}".format(self.data.game_name))
        # assert_true(DUT.Login.base_login_out(), "退出登录", target=DUT)
        # assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        # assert_true(DUT.Login.into_login_page(), "进入游戏中心登录页面", target=DUT)
        # assert_true(DUT.Login.login_in_with_password(account_section="phone_1"), "密码登录", target=DUT)
        assert_true(DUT.Common.back_to_homepage())
        assert_true(DUT.HomePage.into_my_info(), "进入个人中心", target=DUT)

        assert_true(DUT.MyInfoPage.click_tab(self.data.tab_name), "点击小游戏标签", target=DUT)
        assert_true(DUT.MyInfoPage.vertical_game_open(game_name=self.data.game_name), "打开H5游戏", target=DUT)
        time.sleep(5)
        assert_true(DUT.H5Page.check_game_ui(), "检测H5游戏是否打开", target=DUT)
        g_logger.info("重启app，进入游戏中心，用于关闭h5小游戏")
        DUT.Common.reset_app()
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)


    def teardown(self):
        DUT.device.stop_log()

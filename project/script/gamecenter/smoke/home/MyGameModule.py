# -*- coding: UTF-8 -*-

"""
File Name:      MyGameModule
Author:         gufangmei_sx
Create Date:    2018/7/9
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class MyGameModule(TestsuiteNormal):
    """
    用例描述：首页-我的游戏模块-查看全部我的游戏
    预置条件：登录用户最近玩过游戏。
    """
    def setup(self):
        self.desc = "首页-我的游戏模块-查看全部我的游戏"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Login.base_login_out(), "退出登录", target=DUT)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.Login.into_login_page(), "进入游戏中心登录页面", target=DUT)
        assert_true(DUT.Login.login_in_with_password(account_section="phone_1"), "登录", target=DUT)
        assert_true(DUT.Common.back_to_homepage(), "返回游戏中心首页", target=DUT)
        assert_true(DUT.HomePage.into_my_game_module(self.data.my_module, self.data.tab), "进入我的游戏模块", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
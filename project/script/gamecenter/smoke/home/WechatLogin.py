# -*- coding: UTF-8 -*-

"""
File Name:      WechatLogin
Author:         gufangmei_sx
Create Date:    2018/8/9
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class WechatLogin(TestsuiteNormal):
    """
    用例描述：登录-游戏中心-微信登录
    """
    def setup(self):
        self.desc = "登录-游戏中心-微信登录"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Login.base_login_out(), "退出登录", target=DUT)
        g_logger.info("预置条件：手机已安装微信且已登录，并且绑定微信账号，iqiyi授权成功")
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.Login.into_login_page(), "进入个人中心登录页面", target=DUT)
        assert_true(DUT.Login.login_in_with_wechat(), "微信登录", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
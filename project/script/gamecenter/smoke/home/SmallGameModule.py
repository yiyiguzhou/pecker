# -*- coding: UTF-8 -*-

"""
File Name:      SmallGameModule
Author:         gufangmei_sx
Create Date:    2018/7/9
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class SmallGameModule(TestsuiteNormal):
    """
    用例描述：首页-小游戏模块
    预置条件：用户未登录，亚账号最近玩过非棋牌的H5游戏。
    """
    def setup(self):
        self.desc = "首页-小游戏模块"
        DUT.device.start_log()
        DUT.Common.reset_app("com.qiyi.video", "com.qiyi.video.WelcomeActivity")

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("用户未登录，亚账号最近玩过非棋牌的H5游戏。")
        assert_true(DUT.Login.base_login_out(), "退出登录", target=DUT)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.into_small_game_module(), "进入小游戏模块", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

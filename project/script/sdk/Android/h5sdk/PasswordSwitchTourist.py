"""
File Name:      PasswordSwitchTourist.py
Author:         xuxiaofang_sx
Create Date:    2018/8/10
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class PasswordSwitchTourist(TestsuiteNormal):
    """
        用例描述：密码登录页切换游客账号
        预制条件：1.本地没有缓存的手机
                  2.基线登录状态
        """
    def setup(self):
        DUT.device.start_log()
        DUT.H5sdk.start_ipecker_app()
        DUT.H5sdk.reset_app()

    def test(self):
        assert_true(DUT.H5sdk.no_cache(), target=DUT)
        assert_true(DUT.H5sdk.mycount(self.data.phone,self.data.base_password), "基线登陆成功", target=DUT)
        assert_true(DUT.H5sdk.into_game_center(), "进入游戏中心", target=DUT)
        assert_true(DUT.H5sdk.gamecenter_search(self.data.game_text), "进入搜索框成功", target=DUT)
        assert_true(DUT.H5sdk.into_gamedetail(self.data.game_text), "进入游戏详情成功", target=DUT)
        assert_true(DUT.H5sdk.into_h5game(self.data.game_text), "进入非棋牌游戏成功", target=DUT)
        assert_true(DUT.H5sdk.sidebar(self.data.is_tourist, self.data.is_sms, self.data.phone_num), "进入登录",target=DUT)
        assert_true(DUT.H5sdk.password_login(self.data.game_account, self.data.game_password), "密码登录成功", target=DUT)
        assert_true(DUT.H5sdk.sidebar_tourists(), "进入游客登录成功", target=DUT)
        assert_true(DUT.H5sdk.phone_return(), "点击物理返回键成功退出游戏", target=DUT)
        assert_true(DUT.H5sdk.into_h5game(self.data.game_text), "再次进入非棋牌游戏成功")
        assert_true(DUT.H5sdk.account_display(self.data.account_display,self.data.game_account, self.data.game_account), "账号显示正确", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
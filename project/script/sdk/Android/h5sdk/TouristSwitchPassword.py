"""
File Name:      TouristPassword
Author:         xuxiaofang_sx
Create Date:    2018/8/9
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class TouristSwitchPassword(TestsuiteNormal):
    """
        用例描述：游客账号切换密码登录页
        预制条件：1.本地没有缓存的手机
                  2.基线无登录状态
        """
    def setup(self):
        DUT.device.start_log()
        DUT.H5sdk.start_ipecker_app()
        DUT.H5sdk.reset_app()

    def test(self):
        assert_true(DUT.H5sdk.no_cache(), target=DUT)
        assert_true(DUT.H5sdk.gamecenter_search(self.data.game_text), "进入搜索框成功", target=DUT)
        assert_true(DUT.H5sdk.into_gamedetail(self.data.game_text), "进入游戏详情成功", target=DUT)
        assert_true(DUT.H5sdk.into_h5game(self.data.game_text), "进入非棋牌游戏成功", target=DUT)
        assert_true(DUT.H5sdk.guest_login(self.data.game_text), "进入快速游戏", target=DUT)
        assert_true(DUT.H5sdk.sidebar(self.data.is_tourist, self.data.is_sms, self.data.phone_num), "成功进入侧边栏切换账号页面",target=DUT)
        assert_true(DUT.H5sdk.password_login(self.data.game_account, self.data.game_password), "密码登录页成功进入游戏", target=DUT)
        assert_true(DUT.H5sdk.phone_return(), "成功退出游戏", target=DUT)
        assert_true(DUT.H5sdk.into_h5game(self.data.game_text), "再次进入非棋牌游戏成功")
        assert_true(DUT.H5sdk.account_display(self.data.account_display,self.data.game_account, self.data.game_password), "账号显示正确", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
"""
File Name:      BaselineLogin
Author:         xuxiaofang_sx
Create Date:    2018/8/16
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class BaselineLogin(TestsuiteNormal):

    def setup(self):
        """
            用例描述：根据基线账号登录
            预制条件：1.本地没有缓存的手机
                      2.基线有登录状态
                      3.phone：基线手机账号
                      4.base_password：基线账号密码
                      5.game_text：游戏名称
                      6.account_display：账号显示
                      7.game_account：游戏中心账号
                      8.game_password：游戏中心密码
            """
        DUT.device.start_log()
        DUT.H5sdk.start_ipecker_app()
        DUT.H5sdk.reset_app()

    def test(self):
        assert_true(DUT.H5sdk.no_cache(), target=DUT)
        assert_true(DUT.H5sdk.mycount(self.data.phone, self.data.base_password), "基线密账号登陆成功", target=DUT)
        assert_true(DUT.H5sdk.into_game_center(), "进入游戏中心", target=DUT)
        assert_true(DUT.H5sdk.gamecenter_search(self.data.game_text), "进入搜索框成功", target=DUT)
        assert_true(DUT.H5sdk.into_gamedetail(self.data.game_text), "进入游戏详情成功", target=DUT)
        assert_true(DUT.H5sdk.into_h5game(self.data.game_text), "进入非棋牌游戏成功", target=DUT)
        assert_true(DUT.H5sdk.account_display(self.data.account_display,self.data.game_account, self.data.game_password), "根据基线账号登录显示账号正确", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
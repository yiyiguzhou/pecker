"""
File Name:      CacheLogin
Author:         xuxiaofang_sx
Create Date:    2018/8/10
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class CacheLogin(TestsuiteNormal):
    """
        用例描述：缓存登陆
        预制条件：1.本地有缓存
                  game_text：游戏名称
                  account_display：缓存账号（一般基线账号）
                  game_account：游戏中心账号
                  game_password：游戏中心密码
        """
    def setup(self):
        DUT.device.start_log()
        DUT.H5sdk.start_ipecker_app()
        DUT.H5sdk.reset_app()

    def test(self):
        assert_true(DUT.H5sdk.into_game_center(), "进入游戏中心", target=DUT)
        assert_true(DUT.H5sdk.gamecenter_search(self.data.game_text), "进入搜索框成功", target=DUT)
        assert_true(DUT.H5sdk.into_gamedetail(self.data.game_text), "进入游戏详情成功", target=DUT)
        assert_true(DUT.H5sdk.into_h5game(self.data.game_text), "进入非棋牌游戏成功", target=DUT)
        assert_true(DUT.H5sdk.account_display(self.data.account_display,self.data.game_account, self.data.game_password), "缓存账号显示正确", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
"""
File Name:      OrdinaryLogin
Author:         xuxiaofang_sx
Create Date:    2018/8/10
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class OrdinaryLogin(TestsuiteNormal):
    """
        用例描述：普通账号（中文账号）登录
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
        assert_true(DUT.H5sdk.other_login(), "进入其他登录页面", target=DUT)
        assert_true(DUT.H5sdk.password_login(self.data.game_account, self.data.game_password), "普通账号登录成功", target=DUT)

        time.sleep(1)
    def teardown(self):
        DUT.device.stop_log()
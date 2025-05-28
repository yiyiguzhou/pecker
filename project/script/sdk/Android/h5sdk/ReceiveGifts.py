"""
File Name:      ReceiveGifts
Author:         xuxiaofang_sx
Create Date:    2018/8/15
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class ReceiveGifts(TestsuiteNormal):
    """
        用例描述：领取礼包
        预制条件：无
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
        assert_true(DUT.H5sdk.sidebar(self.data.is_tourist, self.data.is_sms, self.data.phone_num), "点击侧边栏切换账号进入普通登录页面成功", target=DUT)
        assert_true(DUT.H5sdk.password_login(self.data.game_account, self.data.game_password), "普通账号登录成功", target=DUT)
        assert_true(DUT.H5sdk.gift(self.data.gift_text), "成功进入礼包领取页面", target=DUT)
        assert_true(DUT.H5sdk.get_gift(self.data.receive,self.data.receive_look), "礼包领取成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

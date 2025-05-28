"""
File Name:      WechatLogin
Author:         xuxiaofang_sx
Create Date:    2018/8/7
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class WechatPay(TestsuiteNormal):
    def setup(self):
        DUT.device.start_log()
        DUT.H5sdk.start_ipecker_app()
        DUT.H5sdk.reset_app()

    def test(self):
        assert_true(DUT.H5sdk.into_game_center(), "进入游戏中心", target=DUT)
        assert_true(DUT.H5sdk.into_mygame_page(self.data.title), "成功进入爱奇艺小游戏", target=DUT)
        time.sleep(5)
        assert_true(DUT.H5sdk.coin(self.data.title), "成功进入小游戏", target=DUT)

        # assert_true(DUT.Mainland.wechat_pay_suss(self.data.account,self.data.password), "微信支付成功", target=DUT)
        # time.sleep(5)
        #assert_true(DUT.Mainland.pay_wechat_confirm(self.data.pay_password,self.data.title), "微信支付成功", target=DUT)
    def teardown(self):
        DUT.device.stop_log()
"""
File Name:      CoinDeductionPay
Author:         xuxiaofang_sx
Create Date:    2018/8/1
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class CoinDeductionPay(TestsuiteNormal):
    """
        用例描述：
        预制条件：
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.start_ipecker_app()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        time.sleep(5)
        assert_true(DUT.Mainland.Coin_DiscountWechatPay(self.data.num,self.data.name), "成功进入支付页面", target=DUT)
        time.sleep(5)

        #assert_true(DUT.Mainland.pay_wechat_confirm(self.data.pay_password,self.data.title), "微信支付成功", target=DUT)
    def teardown(self):
        DUT.device.stop_log()
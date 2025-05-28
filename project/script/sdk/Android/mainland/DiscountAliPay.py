"""
File Name:      DiscountAliPay
Author:         xuxiaofang_sx
Create Date:    2018/8/1
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class DiscountAliPay(TestsuiteNormal):
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
        assert_true(DUT.Mainland.DiscountAliPay(self.data.num), "成功进入支付宝登录页面", target=DUT)
        time.sleep(5)
        #assert_true(DUT.Mainland.Alipay_suss(self.data.title,self.data.account,self.data.password,self.data.pay_password), "支付宝支付成功", target=DUT)
        #time.sleep(5)
        #assert_true(DUT.Mainland.Alipay_login(self.data.account,self.data.password), "支付宝支付页面成功", target=DUT)
    def teardown(self):
        DUT.device.stop_log()
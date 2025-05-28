"""
File Name:      Ali_pay
Author:         xuxiaofang_sx
Create Date:    2018/7/31
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class Alipay(TestsuiteNormal):
    """
        用例描述：支付宝钱包支付
        预制条件：测试的游戏有配置支付渠道
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.start_ipecker_app()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        time.sleep(5)
        assert_true(DUT.Pay.num(self.data.num), "成功进入支付宝登录页面", target=DUT)
        time.sleep(5)
        assert_true(DUT.Pay.pay(self.data.select_pay), "成功进入支付页面", target=DUT)
        assert_true(DUT.Pay.alipay_login(self.data.account,self.data.password,self.data.pay_password), "支付宝支付成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
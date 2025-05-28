"""
File Name:      Pay
Author:         xuxiaofang_sx
Create Date:    2018/7/16
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class WechatPay(TestsuiteNormal):
    """
        用例描述：微信支付
        预制条件：测试的游戏有配置支付渠道
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.start_ipecker_app()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        assert_true(DUT.Pay.wechatpay(self.data.num), "成功进入支付页面", target=DUT)
        time.sleep(2)
        # assert_true(DUT.Pay.wechat_pay_suss(self.data.account,self.data.password), "微信支付成功", target=DUT)
        # time.sleep(2)

    def teardown(self):
        DUT.device.stop_log()
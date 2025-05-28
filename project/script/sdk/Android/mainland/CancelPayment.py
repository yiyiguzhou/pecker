"""
File Name:      CancelPayment
Author:         xuxiaofang_sx
Create Date:    2018/7/18
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class CancelPayment(TestsuiteNormal):
    """
        用例描述：取消支付功能
        预制条件：测试的游戏有配置支付渠道
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        time.sleep(5)
        assert_true(DUT.Mainland.pay_display(self.data.num,self.data.title,self.data.pay_select), "正常跳转到支付页面", target=DUT)
        assert_true(DUT.Mainland.cancel_payment(), "取消支付成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
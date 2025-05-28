"""
File Name:      Pay2
Author:         xuxiaofang_sx
Create Date:    2018/7/18
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class Pay2(TestsuiteNormal):
    """
        用例描述：
        预制条件：
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        time.sleep(5)
        assert_true(DUT.Mainland.pay(self.data.num), "支付成功", target=DUT)
        time.sleep(5)
        assert_true(DUT.Mainland.mobile_phone_return(), "手机返回成功", target=DUT)
        time.sleep(5)
        assert_true(DUT.Mainland.pay(self.data.num), "支付成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
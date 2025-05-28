"""
File Name:      NoAccountCorrect
Author:         xuxiaofang_sx
Create Date:    2018/7/27
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class NoAccountCorrect(TestsuiteNormal):
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

        assert_true(DUT.Mainland.mobilelogin_sms(self.data.vip_time,self.data.phone), "手机登录页面成功", target=DUT)
        assert_true(DUT.Mainland.Account_correct(self.data.text), "自动登录账号显示成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
"""
File Name:      MobilePhoneReturn
Author:         xuxiaofang_sx
Create Date:    2018/7/18
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class MobilePhoneReturn(TestsuiteNormal):
    """
        用例描述：
        预制条件：
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.start_ipecker_app()
        DUT.Mainland.reset_app()

    def test(self):

        assert_true(DUT.Mainland.mobile_phone_return(), "手机退出页面显示正常", target=DUT)

        # assert_true(DUT.Mainland.login_sms(self.data.phone),"手机登录",target=DUT)
        # assert_true(DUT.Demo.logout(), "退出登录")
        # assert_true(DUT.Demo.login_sms(self.data.phone), "初始化微信登录")
        # assert_true(DUT.Demo.logout(), "退出登录")

    def teardown(self):
        DUT.device.stop_log()
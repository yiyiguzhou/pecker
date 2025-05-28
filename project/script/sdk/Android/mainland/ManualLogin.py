"""
File Name:      ManualLogin
Author:         xuxiaofang_sx
Create Date:    2018/7/16
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class ManualLogin(TestsuiteNormal):
    """
        用例描述：
        预制条件：
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        assert_true(DUT.Mainland.manual_login(self.data.account, self.data.password), "手动登录页面", target=DUT)
        # assert_true(DUT.Mainland.login_sms(self.data.phone),"手机登录",target=DUT)
        # assert_true(DUT.Demo.logout(), "退出登录")
        # assert_true(DUT.Demo.login_sms(self.data.phone), "初始化微信登录")
        # assert_true(DUT.Demo.logout(), "退出登录")

    def teardown(self):
        DUT.device.stop_log()
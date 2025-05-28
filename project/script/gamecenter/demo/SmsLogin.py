# -*- coding: UTF-8 -*-

"""
File Name:      SmsLogin
Author:         zhangwei04
Create Date:    2018/4/9
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class SmsLogin(TestsuiteNormal):
    def setup(self):
        DUT.Demo.start_ipecker_app()
        DUT.Demo.reset_app()

    def test(self):
        assert_true(DUT.Demo.into_user_info(), "进入基线用户信息页面")
        assert_true(DUT.Demo.login_sms(self.data.phone), "初始化微信登录")
        assert_true(DUT.Demo.logout(), "退出登录")

    def teardown(self):
        pass

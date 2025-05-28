"""
File Name:      AccountPasswordLogin
Author:         xuxiaofang_sx
Create Date:    2018/7/20
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class Authentication(TestsuiteNormal):
    """
        用例描述：
        预制条件：
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        assert_true(DUT.Mainland.account_password_login(self.data.account,self.data.password),"账号密码登录成功",target=DUT)

    def teardown(self):
        DUT.device.stop_log()
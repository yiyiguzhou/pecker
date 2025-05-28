# -*- coding: UTF-8 -*-

"""
File Name:      AuthPresure
Author:         zhangwei04
Create Date:    2018/3/12
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class LoginPressure(TestsuiteNormal):
    def setup(self):
        DUT.device.start_log()

    def test(self):
        # assert_true(DUT.Demo.into_gamecenter())
        # assert_true(DUT.Demo.into_gamecenter_user_info())
        # assert_true(DUT.Demo.gamecenter_login_passwd())
        g_logger.info('this is test demo')
        DUT.Demo.reset_app()
        assert_true(DUT.Demo.into_user_info(), "进入基线用户信息页面")
        assert_true(DUT.Demo.login_passwd(self.data.username, self.data.password), "密码方式登录")
        assert_true(DUT.Demo.logout(), "退出登录")

    def teardown(self):
        DUT.device.stop_log()

"""
File Name:      EmailPasswordRecovery.py
Author:         xuxiaofang_sx
Create Date:    2018/7/20
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class EmailPasswordRecovery(TestsuiteNormal):
    """
        用例描述：邮箱找回密码
        预制条件：有缓存
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.start_ipecker_app()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        assert_true(DUT.Sidebar.Sidebar_display(), "侧边栏显示", target=DUT)
        assert_true(DUT.Registered.Other_login(self.data.vip_time), "其他登录方式显示成功", target=DUT)
        assert_true(DUT.Login.Other_login_retrieve_password_email(), "邮箱找回密码成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
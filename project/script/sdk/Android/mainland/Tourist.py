"""
File Name:      Tourists
Author:         xuxiaofang_sx
Create Date:    2018/7/18
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class Tourist(TestsuiteNormal):
    """
        用例描述：游客登录
        预制条件：无
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        time.sleep(3)
        assert_true(DUT.Mainland.Tourist_login(), "自动登录成功", target=DUT)
        time.sleep(3)
        assert_true(DUT.Mainland.Account_correct(self.data.text), "自动登录账号显示成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
"""
File Name:      ThirdLoginbaidu.py
Author:         xuxiaofang_sx
Create Date:    2018/7/25
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class ThirdLoginbaidu(TestsuiteNormal):
    """
        用例描述：第三方百度登录
        预制条件：无
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.start_ipecker_app()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        assert_true(DUT.Mainland.Other_login(), "其他登录页面显示", target=DUT)
        assert_true(DUT.Mainland.third_login_baidu(self.data.account,self.data.password), "第三方百度登陆成功", target=DUT)
        # assert_true(DUT.Mainland.login_sms(self.data.phone),"手机登录",target=DUT)
        # assert_true(DUT.Demo.logout(), "退出登录")
        # assert_true(DUT.Demo.login_sms(self.data.phone), "初始化微信登录")
        # assert_true(DUT.Demo.logout(), "退出登录")

    def teardown(self):
        DUT.device.stop_log()
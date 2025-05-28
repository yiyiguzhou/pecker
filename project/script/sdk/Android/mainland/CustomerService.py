"""
File Name:      CustomerService
Author:         xuxiaofang_sx
Create Date:    2018/8/7
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class CustomerService(TestsuiteNormal):
    """
        用例描述：密码登录页面客服显示功能
        预制条件：vip_time：游戏会员登录，会员到期时间
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.start_ipecker_app()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        assert_true(DUT.Sidebar.Sidebar_display(), "侧边栏显示", target=DUT)
        assert_true(DUT.Registered.Other_login(self.data.vip_time), "其他登录方式显示成功", target=DUT)
        assert_true(DUT.Login.customer(), "客服页面显示", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
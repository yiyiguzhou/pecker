"""
File Name:      ThirdLogin
Author:         xuxiaofang_sx
Create Date:    2018/7/20
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class ThirdLoginsina(TestsuiteNormal):
    """
        用例描述：第三方新浪账号登陆
        预制条件：vip_time：会员到期时间
                  account：新浪账号
                  password：新浪密码
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.start_ipecker_app()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        assert_true(DUT.Registered.Other_login(self.data.vip_time), "其他登录页面显示", target=DUT)
        assert_true(DUT.Mainland.third_login_sina(self.data.account,self.data.password), "第三方新浪登陆成功", target=DUT)
        assert_true(DUT.Registered.initialize_wetchat_login(), "初始化微信登陆", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
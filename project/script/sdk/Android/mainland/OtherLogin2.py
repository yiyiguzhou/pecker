"""
File Name:      OtherLogin2
Author:         xuxiaofang_sx
Create Date:    2018/7/27
"""
import time
from project.script.testsuite.TestsuiteNormal import *

class OtherLogin2(TestsuiteNormal):
    """
        用例描述：账号密码登录二次登录也可成功
        预制条件：vip_time：会员到期时间
                  account：登录账号
                  password：登录密码
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.start_ipecker_app()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        assert_true(DUT.Registered.Other_login(self.data.vip_time), "其他登录页面显示", target=DUT)
        assert_true(DUT.Registered.account_password_login(self.data.account, self.data.password), "账号密码登陆成功", target=DUT)
        time.sleep(2)
        assert_true(DUT.Registered.Other_login(self.data.vip_time), "其他登录页面显示", target=DUT)
        assert_true(DUT.Registered.account_password_login(self.data.account, self.data.password), "账号密码二次登陆成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
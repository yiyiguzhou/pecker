"""
File Name:      OtherLlogin
Author:         xuxiaofang_sx
Create Date:    2018/7/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class OtherLogin(TestsuiteNormal):
    """
        用例描述：账号密码登录与注册
        预制条件：手机有爱奇艺游戏用户缓存
                  vip_time：会员到期时间
                  account：普通账号
                  password：普通密码
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.start_ipecker_app()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        assert_true(DUT.Registered.Other_login(self.data.vip_time), "其他登录页面显示", target=DUT)
        assert_true(DUT.Registered.account_password_login(self.data.account, self.data.password), "账号密码登陆成功", target=DUT)


    def teardown(self):
        DUT.device.stop_log()
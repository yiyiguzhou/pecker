"""
File Name:      Authentication
Author:         xuxiaofang_sx
Create Date:    2018/7/11
"""


import time
from project.script.testsuite.TestsuiteNormal import *


class Authentication(TestsuiteNormal):
    """
        用例描述：未实名认证用户登录进行实名认证
        预制条件：1.使用未身份实名认证用户登录
                  2.身份证实名认证验配开关为开启
                 （position_id为23或者是24）
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        # assert_true(DUT.Mainland.Other_login(self.data.vip_time), "其他登录页面显示", target=DUT)
        # assert_true(DUT.Mainland.account_password_login(self.data.account, self.data.password), "账号密码登陆成功", target=DUT)
        assert_true(DUT.Mainland.id_verified(self.data.user_name,self.data.id_card,self.data.is_identify),"身份认证成功",target=DUT)
        # assert_true(DUT.Demo.login_sms(self.data.phone), "初始化微信登录")
        # assert_true(DUT.Demo.logout(), "退出登录")

    def teardown(self):
        DUT.device.stop_log()
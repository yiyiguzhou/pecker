"""
File Name:      WetchatLogin
Author:         xuxiaofang_sx
Create Date:    2018/7/18
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class WetchatLogin(TestsuiteNormal):
    """
        用例描述：微信登录
        预制条件：1.该游戏支付微信授权登录
                  2.手机上有安装微信app,并且是已登录状态
                  3.vip_time：会员到期时间
                  4.wechat_account：微信账号
                  5。wechat_password：微信密码

        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        assert_true(DUT.Registered.initialize_wetchat_login(), "初始化微信登陆", target=DUT)
        assert_true(DUT.Registered.Other_login(self.data.vip_time), "其他登录方式显示成功", target=DUT)
        assert_true(DUT.Registered.wetchat_login(self.data.wechat_account,self.data.wechat_password), "微信登陆成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
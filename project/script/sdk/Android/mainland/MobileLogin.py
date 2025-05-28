"""
File Name:      iqylogin
Author:         xuxiaofang_sx
Create Date:    2018/7/11
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class MobileLogin(TestsuiteNormal):
    """
        用例描述：用手机账号登录
        预制条件：vip_time：会员到期时间
                  phone：手机号
                  手机有爱奇艺游戏用户缓存
        """
    def setup(self):
        DUT.device.start_logcat()
        DUT.Mainland.start_ipecker_app()
        DUT.Mainland.reset_app()
    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        assert_true(DUT.Registered.Other_login(self.data.vip_time), "其他登录方式显示成功", target=DUT)
        assert_true(DUT.Registered.mobilelogin_sms(self.data.phone), "手机登录页面成功", target=DUT)
        assert_true(DUT.Registered.initialize_wetchat_login(), "进入游戏成功", target=DUT)

    def teardown(self):
        DUT.device.stop_logcat()
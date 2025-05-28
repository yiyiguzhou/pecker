"""
File Name:      MobileAuthentication
Author:         xuxiaofang_sx
Create Date:    2018/7/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class MobileAuthentication(TestsuiteNormal):
    """
        用例描述：
        预制条件：
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.start_ipecker_app()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        # assert_true(DUT.Mainland.id_verified(self.data.user_name,self.data.id_card),"身份认证成功",target=DUT)
        assert_true(DUT.Mainland.mobile_real_authentication(self.data.phone),"手机实名认证成功",target=DUT)
        assert_true(DUT.Mainland.Account_correct(self.data.text), "自动登录账号显示成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
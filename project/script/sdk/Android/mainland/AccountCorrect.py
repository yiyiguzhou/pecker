"""
File Name:      AccountCorrect
Author:         xuxiaofang_sx
Create Date:    2018/7/25
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class AccountCorrect(TestsuiteNormal):
    """
    用例描述：缓存账号登录
    预制条件：手机有爱奇艺游戏用户缓存
              cache_account：缓存账号
    """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        assert_true(DUT.Registered.Account_correct(self.data.cache_account), "自动登录账号显示成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
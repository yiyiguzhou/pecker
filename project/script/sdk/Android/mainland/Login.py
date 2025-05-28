"""
File Name:      Login
Author:         xuxiaofang_sx
Create Date:    2018/7/11
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class Login(TestsuiteNormal):
    """
        用例描述：1.手机无爱奇艺游戏用户缓存
        预制条件：1.奇玩后台极速登录云配开关为开启（（position_id：43为开启）
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.reset_app()
        DUT.Mainland.clear_app_data("com.iqiyigame.sdk.demo")

    def test(self):
        assert_true(DUT.Mainland.no_cache())
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
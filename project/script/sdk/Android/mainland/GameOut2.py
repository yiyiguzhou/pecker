"""
File Name:      GameOut2
Author:         xuxiaofang_sx
Create Date:    2018/7/23
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class GameOut2(TestsuiteNormal):
    """
        用例描述：物理返回键退出游戏
        预制条件：无
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.reset_app()

    def test(self):

        assert_true(DUT.Exit.mobile_phone_return2(), "游戏退出成功页面", target=DUT)


    def teardown(self):
        DUT.device.stop_log()
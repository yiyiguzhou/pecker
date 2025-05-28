"""
File Name:      GameMembershipCardPage
Author:         xuxiaofang_sx
Create Date:    2018/8/8
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class GameMembershipCardPage(TestsuiteNormal):
    """
        用例描述：
        预制条件：
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        assert_true(DUT.Mainland.game_vip_page(), "会员卡购买页面显示正常", target=DUT)


    def teardown(self):
        DUT.device.stop_log()